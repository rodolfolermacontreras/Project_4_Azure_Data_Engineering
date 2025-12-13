#!/usr/bin/env python3
"""
Query Synapse using OPENROWSET to read partition files directly
"""

import pyodbc
import pandas as pd

SYNAPSE_SERVER = "synapse-nycpayroll-rodolfo-l-ondemand.sql.azuresynapse.net"
DATABASE = "udacity"
USERNAME = "sqladmin"
PASSWORD = "P@ssw0rd1234!"

print("Querying dirstaging partition files using OPENROWSET...")
print()

conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SYNAPSE_SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};Encrypt=yes;TrustServerCertificate=no"
conn = pyodbc.connect(conn_str)

# Query using OPENROWSET with full storage path
query = """
SELECT 
    FiscalYear,
    AgencyName,
    TotalPaid
FROM OPENROWSET(
    BULK 'https://adlsnycpayrollrodolfol.dfs.core.windows.net/dirstaging/part-*.csv',
    FORMAT = 'CSV',
    PARSER_VERSION = '2.0',
    HEADER_ROW = TRUE
) WITH (
    FiscalYear INT,
    AgencyName VARCHAR(200) COLLATE Latin1_General_100_CI_AS_SC_UTF8,
    TotalPaid FLOAT
) AS [result]
ORDER BY TotalPaid DESC
"""

try:
    df = pd.read_sql(query, conn)
    
    print(f"✓ Total records: {len(df)}")
    print(f"✓ Fiscal years: {sorted(df['FiscalYear'].unique().tolist())}")
    print()
    print("Top 10 agencies by total paid:")
    print(df.head(10).to_string(index=False))
    print()
    print("✓ Synapse query successful using OPENROWSET")
    
except Exception as e:
    print(f"✗ Error: {str(e)}")

conn.close()

print()
print("=" * 80)
print("For screenshot: Use this query in Synapse Studio:")
print("=" * 80)
print(query)
