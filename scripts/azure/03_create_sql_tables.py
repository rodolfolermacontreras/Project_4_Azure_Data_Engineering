"""
Step 3: Create SQL Database Tables

WHY THIS MATTERS:
Before data pipelines can load data, the destination tables must exist.
This script creates all 6 tables in Azure SQL Database:
- 3 Master Data tables (dimension tables)
- 2 Payroll transaction tables (fact tables)
- 1 Summary table (aggregated data)

For Data Scientists: In relational databases, you define the schema
(structure) before loading data. This ensures data quality and enables
SQL queries with joins and aggregations.
"""

import subprocess
import os

# Configuration
SQL_SERVER_NAME = "sqlserver-nycpayroll-rodolfo-l.database.windows.net"
SQL_DB_NAME = "db_nycpayroll"
SQL_ADMIN_USER = "sqladmin"
SQL_ADMIN_PASSWORD = "P@ssw0rd1234!"

# Get path to SQL script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
SQL_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "sql", "01_create_sqldb_tables.sql")

def run_sql_script():
    """
    Execute SQL script to create all tables
    
    WHY USE SQLCMD:
    - Direct connection to Azure SQL Database
    - Can execute multiple statements in one script
    - Industry-standard tool for SQL Server administration
    
    ALTERNATIVE METHODS:
    - Azure Data Studio (GUI tool)
    - SQL Server Management Studio (SSMS)
    - Python pyodbc library
    - Azure Portal Query Editor
    """
    print(f"\n{'='*70}")
    print("CREATING SQL DATABASE TABLES")
    print(f"{'='*70}")
    
    print(f"\nServer: {SQL_SERVER_NAME}")
    print(f"Database: {SQL_DB_NAME}")
    print(f"User: {SQL_ADMIN_USER}")
    print(f"\nExecuting script: {SQL_SCRIPT}")
    
    # Build sqlcmd command
    command = f'''sqlcmd -S {SQL_SERVER_NAME} -d {SQL_DB_NAME} -U {SQL_ADMIN_USER} -P "{SQL_ADMIN_PASSWORD}" -i "{SQL_SCRIPT}" -I'''
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print("\nSUCCESS!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: {e.stderr}")
        print("\nIf sqlcmd is not installed, you can:")
        print("1. Install SQL Server Command Line Tools from Microsoft")
        print("2. Use Azure Portal Query Editor instead")
        print("3. Use Azure Data Studio")
        return False

def verify_tables():
    """
    Verify all 6 tables were created
    
    WHY VERIFICATION MATTERS:
    - Confirms script executed successfully
    - Ensures pipelines will have valid destinations
    - Catches schema errors before pipeline development
    """
    print(f"\n{'='*70}")
    print("VERIFYING TABLE CREATION")
    print(f"{'='*70}")
    
    # Query to list all tables
    verify_query = """
    SELECT 
        TABLE_NAME,
        (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = t.TABLE_NAME) as COLUMN_COUNT
    FROM INFORMATION_SCHEMA.TABLES t
    WHERE TABLE_TYPE = 'BASE TABLE'
    ORDER BY TABLE_NAME;
    """
    
    command = f'''sqlcmd -S {SQL_SERVER_NAME} -d {SQL_DB_NAME} -U {SQL_ADMIN_USER} -P "{SQL_ADMIN_PASSWORD}" -Q "{verify_query}" -h-1'''
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print("\nTables created:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr}")
        return False

def print_summary():
    """Print summary with data engineering concepts"""
    print(f"\n{'='*70}")
    print("SQL TABLES CREATED SUCCESSFULLY")
    print(f"{'='*70}")
    
    print("""
DATABASE SCHEMA EXPLANATION:

DIMENSION TABLES (Master Data):
1. AGENCY_MD
   - AgencyID (Primary Key)
   - AgencyName
   WHY: Agency is a dimension - describes WHO (which government agency)
   
2. EMP_MD
   - EmployeeID (Primary Key)
   - FirstName, LastName
   WHY: Employee is a dimension - describes WHO (which employee)
   
3. TITLE_MD
   - TitleCode (Primary Key)
   - TitleDescription
   WHY: Title is a dimension - describes WHAT (job position)

FACT TABLES (Transaction Data):
4. NYC_Payroll_2020
   - FiscalYear, PayrollNumber (Composite Key)
   - Foreign Keys: AgencyID, EmployeeID, TitleCode
   - Measures: BaseSalary, RegularGrossPaid, TotalOTPaid, TotalOtherPay
   WHY: Contains historical payroll transactions
   
5. NYC_Payroll_2021
   - Same structure as 2020
   WHY: Contains current year payroll transactions

SUMMARY TABLE (Aggregated/Gold Layer):
6. NYC_Payroll_Summary
   - FiscalYear, AgencyName (Composite Key)
   - TotalPaid (SUM of all payments)
   WHY: Pre-aggregated for fast reporting and public transparency

DATA WAREHOUSE CONCEPTS:
- Star Schema: Fact tables in center, dimension tables around
- Surrogate Keys: Integer IDs for efficient joins
- Denormalization: AgencyName in summary for query performance
- Separation: Historical vs Current for data lifecycle management

NEXT STEP: Create Synapse external table to query summary data
""")

def main():
    """Execute SQL table creation"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║              CREATE SQL DATABASE TABLES                           ║
    ║                Schema Definition Phase                            ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if SQL script exists
    if not os.path.exists(SQL_SCRIPT):
        print(f"ERROR: SQL script not found: {SQL_SCRIPT}")
        return
    
    print("\nThis script will create 6 tables in Azure SQL Database.")
    print("Estimated time: 1 minute")
    
    input("\nPress Enter to start...")
    
    # Create tables
    if run_sql_script():
        # Verify
        verify_tables()
        
        # Print summary
        print_summary()
        
        print("\nNEXT STEP: Create Synapse external table using script 04_create_synapse_external_table.py")
    else:
        print("\nFailed to create tables. Please check error messages above.")
        print("\nALTERNATIVE: Run the SQL script manually in Azure Portal Query Editor")

if __name__ == "__main__":
    main()
