#!/usr/bin/env python3
"""
Fix Synapse external table to read from partition files
"""

import pyodbc

SYNAPSE_SERVER = "synapse-nycpayroll-rodolfo-l-ondemand.sql.azuresynapse.net"
DATABASE = "udacity"
USERNAME = "sqladmin"
PASSWORD = "P@ssw0rd1234!"

print("Fixing Synapse external table...")
print()

conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SYNAPSE_SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};Encrypt=yes;TrustServerCertificate=no"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Drop and recreate external table
print("Dropping old external table...")
try:
    cursor.execute("DROP EXTERNAL TABLE dbo.NYC_Payroll_Summary")
    conn.commit()
    print("✓ Dropped")
except:
    print("✓ Table doesn't exist or already dropped")

print("Creating new external table pointing to dirstaging folder...")
create_sql = """
CREATE EXTERNAL TABLE dbo.NYC_Payroll_Summary (
    FiscalYear INT,
    AgencyName VARCHAR(200),
    TotalPaid FLOAT
)
WITH (
    LOCATION = 'dirstaging/',
    DATA_SOURCE = ExternalDataSourcePayroll,
    FILE_FORMAT = SynapseDelimitedTextFormat
)
"""
cursor.execute(create_sql)
conn.commit()
print("✓ Created")

print()
print("Testing query...")
cursor.execute("SELECT TOP 5 FiscalYear, AgencyName, TotalPaid FROM dbo.NYC_Payroll_Summary ORDER BY TotalPaid DESC")
rows = cursor.fetchall()

print()
print("Top 5 results:")
for row in rows:
    print(f"  {row.FiscalYear} | {row.AgencyName} | ${row.TotalPaid:,.2f}")

conn.close()

print()
print("✓ Synapse external table fixed and verified")
