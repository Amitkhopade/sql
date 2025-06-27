# This script uses the Anthropic Claude API to convert natural language queries into SQL Server queries or stored procedures.
import sys
import anthropic
import pyodbc
import pandas as pd

# ✅ Configuration
anthropic_client = anthropic.Anthropic(api_key="your_API_KEY")
database = "retaildata" # Replace with your database name
server = "MOHINI\SQLEXPRESS"  # Replace with your SQL Server instance

# ✅ Step 1: Get natural language query
if len(sys.argv) < 2:
    print("❌ Please provide a natural language query.")
    sys.exit(1)

nl_query = sys.argv[1]

# ✅ Step 2: Connect to SQL Server
conn = pyodbc.connect(
    f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
)
cursor = conn.cursor()

# ✅ Step 3: Get full schema for all tables
def get_full_schema(cursor):
    schema = ""
    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
    """)
    tables = cursor.fetchall()

    for (table,) in tables:
        schema += f"\n-- Table: {table}\n"
        cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table}'
        """)
        columns = cursor.fetchall()
        for col_name, col_type in columns:
            schema += f"{col_name}: {col_type}\n"
    return schema

full_schema = get_full_schema(cursor)

# ✅ Step 4: Build intelligent prompt
prompt = f"""
You are a highly skilled and professional SQL Developer working on enterprise-grade databases in Microsoft SQL Server.

Your role includes:
1. Understanding and interpreting natural language questions or business problems.
2. Analyzing full database schemas including multiple tables, relationships, data types, and constraints.
3. Writing efficient, clean, and scalable T-SQL queries, views, stored procedures, and scripts.
4. Adding developer-friendly comments explaining the logic, structure, and purpose of each query block.
5. Suggesting optimization techniques when necessary, such as using indexes, avoiding subqueries, and efficient JOINs.
6. Following SQL Server best practices: aliasing, meaningful names, proper formatting, avoiding SELECT *.
7. Understanding stored procedure structure, including parameters, input validation, and error handling.
8. Writing scripts that can be executed directly in SQL Server Management Studio.

Knowledge you must demonstrate includes:
- T-SQL syntax, including DDL, DML, joins, window functions, CTEs, and subqueries.
- Stored procedure creation and execution.
- Working with INFORMATION_SCHEMA and metadata for table introspection.
- Handling NULLs, data type conversions, and error handling in SQL Server.
- Applying indexes and understanding execution plans (conceptually).
- Producing clean output suitable for BI dashboards or further analysis.

Your ideal audience includes:
- Business Analysts, Data Engineers, or Database Administrators.
- Junior SQL developers seeking to learn best practices.
- Power users who know business logic but not how to write SQL.

When answering, always:
- Include only the final T-SQL code (unless otherwise asked).
- Add inline comments to explain what each section does.
- Prefer clarity and maintainability over unnecessary complexity.
- Respond like a mentor or lead developer writing production-ready SQL code.

---

Below is the database schema:

{full_schema}

Now, based on the above schema, respond to the following request:

"{nl_query}"

Write either:
1. A complete SQL Server query, or
2. A full stored procedure (if the task is more suitable that way)

Include meaningful comments and return only the SQL code.
"""


# ✅ Step 5: Use Claude to generate response
response = anthropic_client.messages.create(
    model="claude-3-opus-20240229",  # Or use claude-3-sonnet-20240229 for cost savings
    max_tokens=1000,
    temperature=0,
    messages=[{"role": "user", "content": prompt}]
)

generated_sql = response.content[0].text.strip()
print("\n🧠 Generated SQL / Stored Procedure:\n")
print(generated_sql)

# ✅ Step 6: (Optional) Execute SELECT queries only
if generated_sql.lower().strip().startswith("select"):
    try:
        cursor.execute(generated_sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

        print("\n📊 Query Result:\n")
        print(df.to_string(index=False))

    except Exception as e:
        print("\n❌ Failed to execute SQL:")
        print(e)
