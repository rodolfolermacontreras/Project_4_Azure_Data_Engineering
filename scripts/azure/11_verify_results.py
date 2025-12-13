#!/usr/bin/env python3
"""
Step 8: Verify Pipeline Results

Queries SQL DB, checks Data Lake, and queries Synapse to verify data loaded correctly.
"""

import pyodbc
import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import AzureCliCredential

# Configuration
SQL_SERVER = "sqlserver-nycpayroll-rodolfo-l.database.windows.net"
SQL_DATABASE = "db_nycpayroll"
SQL_USERNAME = "sqladmin"
SQL_PASSWORD = "P@ssw0rd1234!"
STORAGE_ACCOUNT = "adlsnycpayrollrodolfol"
CONTAINER = "dirstaging"

print("=" * 80)
print("STEP 8: Verifying Pipeline Results")
print("=" * 80)
print()

# 1. Verify SQL Database
print("1. Checking SQL Database: NYC_Payroll_Summary")
print("-" * 80)

try:
    conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USERNAME};PWD={SQL_PASSWORD};Encrypt=yes;TrustServerCertificate=no"
    conn = pyodbc.connect(conn_str)
    
    # Query summary table
    query = """
    SELECT 
        FiscalYear,
        AgencyName,
        TotalPaid
    FROM NYC_Payroll_Summary
    ORDER BY FiscalYear, TotalPaid DESC
    """
    
    df = pd.read_sql(query, conn)
    
    print(f"✓ Total records: {len(df)}")
    print(f"✓ Fiscal years: {df['FiscalYear'].unique().tolist()}")
    print()
    print("Top 5 agencies by total paid:")
    print(df.head(5).to_string(index=False))
    print()
    
    # Also check row counts in all tables
    tables = [
        'NYC_Payroll_AGENCY_MD',
        'NYC_Payroll_EMP_MD', 
        'NYC_Payroll_TITLE_MD',
        'NYC_Payroll_Data_2020',
        'NYC_Payroll_Data_2021',
        'NYC_Payroll_Summary'
    ]
    
    print("Row counts for all tables:")
    for table in tables:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count:,} rows")
    
    conn.close()
    print("✓ SQL Database verification complete")
    
except Exception as e:
    print(f"✗ SQL Database error: {str(e)}")

print()
print()

# 2. Verify Data Lake
print("2. Checking Data Lake: dirstaging container")
print("-" * 80)

try:
    credential = AzureCliCredential()
    service_client = DataLakeServiceClient(
        account_url=f"https://{STORAGE_ACCOUNT}.dfs.core.windows.net",
        credential=credential
    )
    
    file_system_client = service_client.get_file_system_client(CONTAINER)
    paths = file_system_client.get_paths()
    
    files_found = []
    for path in paths:
        if not path.is_directory:
            files_found.append(path.name)
            print(f"✓ Found file: {path.name}")
    
    if "NYC_Payroll_Summary.csv" in files_found:
        print()
        print("✓ NYC_Payroll_Summary.csv exists in dirstaging")
    else:
        print()
        print("✗ NYC_Payroll_Summary.csv NOT FOUND in dirstaging")
    
    print("✓ Data Lake verification complete")
    
except Exception as e:
    print(f"✗ Data Lake error: {str(e)}")

print()
print()

# 3. Verify Synapse
print("3. Checking Synapse: External table")
print("-" * 80)

try:
    # Synapse serverless connection
    synapse_server = "synapse-nycpayroll-rodolfo-l-ondemand.sql.azuresynapse.net"
    synapse_database = "udacity"
    
    conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={synapse_server};DATABASE={synapse_database};UID={SQL_USERNAME};PWD={SQL_PASSWORD};Encrypt=yes;TrustServerCertificate=no"
    conn = pyodbc.connect(conn_str)
    
    query = """
    SELECT 
        FiscalYear,
        AgencyName,
        TotalPaid
    FROM dbo.NYC_Payroll_Summary
    ORDER BY FiscalYear, TotalPaid DESC
    """
    
    df = pd.read_sql(query, conn)
    
    print(f"✓ Total records: {len(df)}")
    print(f"✓ Fiscal years: {df['FiscalYear'].unique().tolist()}")
    print()
    print("Top 5 agencies from Synapse:")
    print(df.head(5).to_string(index=False))
    
    conn.close()
    print()
    print("✓ Synapse external table verification complete")
    
except Exception as e:
    print(f"✗ Synapse error: {str(e)}")

print()
print("=" * 80)
print("VERIFICATION COMPLETE!")
print("=" * 80)
print()
print("Screenshots needed:")
print("  - step8_sqldb_summary_query.png (SQL query results)")
print("  - step8_dirstaging_files.png (Data Lake files)")
print("  - step8_synapse_query.png (Synapse query results)")
