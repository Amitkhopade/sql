# Sql Agent to read database and write a sql query.

This agent will read the database and understand the table structure and schema & provide the sql query also it will provide store procedure.
if any one would like to use at enterpise level CPU & GPU is not a constrint then you can use SQLCoder‑34B (≈84%), Arctic‑Text2SQL‑R1‑7B (SOTA Bird), CodeS‑15B (≈86% Spider).
however I prefered to use anothopric model since it has high accuracy if you would like to use only for local perpose.

i installed libary
pip pyodbc pandas anthropic sys.

if you would like to run use sql.py " then your query" 
also you should have microsoft server management studio to have your server details.
ig any help needed 

creating a table was one challenge i come across so take out any kaggle datase download it on local machine & put that file in the C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\ path.
then use below sql commond to upload it on the sql sever. i used other methods as well using import functions but i was getting error this method is quite easy to do it.
Make sure table is created with your rows & if you prefered to write it by own you can use create command if no then you know the answer.

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

Advise- Do not directly copy paste query i did it & boom, i deleted entire table lol :)

#Future possiblity.

add another agent who will read all the database and table those are running on the sql server & it wiill store update the disciption then our agent to write a quqery.
since LLM will not able to understand all entire server table and databases.
also, you can built using stremlit and flask for using thr user interface extend the possiblities to resolve the bugs.

contact@#KHOPADE.AMIT91@GMAIL.COM

