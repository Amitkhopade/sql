 SQL Developer Agent – Overview
This agent is designed to connect to your SQL Server database, read the table structure and schema, and intelligently generate SQL queries or stored procedures in response to natural language questions.

For local or enterprise-level use, you can customize the underlying LLM based on your requirements:

🧠 Model Options
✅ SQLCoder‑34B (≈84% accuracy) — large and ideal for enterprise usage with CPU/GPU resources

✅ Arctic‑Text2SQL‑R1‑7B (SOTA, Bird benchmark) — lightweight and effective

✅ CodeS‑15B (≈86% on Spider) — another strong candidate for production-level tasks

However, for local personal use, I preferred using Anthropic Claude (e.g., Claude 3.5) due to its high accuracy and reliability without needing GPU-intensive setup.

🖥️ Environment Setup
Ensure the following libraries are installed:

bash
Copy
Edit
pip install pyodbc pandas anthropic
▶️ Running the Agent from Terminal or PowerShell
To run the agent and get a SQL query from a natural language question:

bash
Copy
Edit
python sql.py "Show total orders from Germany over the last 30 days"
You must have Microsoft SQL Server Management Studio (SSMS) installed to access your SQL Server instance and get the correct connection details (server name, database name, etc.).

📥 Uploading Bulk Data to SQL Server
Creating tables was one of the early challenges I encountered. I suggest downloading any structured dataset (e.g., from Kaggle), saving it locally, and then using the BULK INSERT command.

⚠️ Place your CSV file at this location:
C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\

Then use the following T-SQL command to insert data:

sql
Copy
Edit
BULK INSERT CustomerOrders
FROM 'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\yourfilename.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK,
    CODEPAGE = '65001',
    FORMAT = 'CSV'
);
✅ Tip: Before running the BULK INSERT, ensure your table (CustomerOrders) is already created with the correct column names and data types that match the CSV file. You can create it manually using CREATE TABLE or through SSMS.

⚠️ Caution: Do not blindly copy-paste queries into your SQL editor. I once mistakenly ran a query that deleted the entire table. Always double-check before executing critical operations!

🔮 Future Possibilities
You can further expand this agent by:

Creating another agent that scans all databases and tables running on your SQL Server instance.

Auto-generating or updating table descriptions, which will enhance LLM understanding.

Building a Streamlit or Flask interface to make it more user-friendly and interactive.

Extending error handling, logging, and prompt optimization to make it production-ready.

This could eventually evolve into a complete AI-powered assistant for database developers, analysts, and support teams.

📧 For questions or help:
contact: khopade.amit91@gmail.com
