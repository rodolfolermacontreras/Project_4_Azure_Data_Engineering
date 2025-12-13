"""
Step 1: Create Azure Infrastructure for NYC Payroll Data Analytics

This script creates all required Azure resources:
1. Azure Data Lake Storage Gen2 (ADLS Gen2) with hierarchical namespace
2. Azure SQL Database
3. Azure Data Factory
4. Azure Synapse Analytics workspace

Each resource is explained for learning purposes.
"""

import subprocess
import json
import sys

# Configuration - Udacity Lab Environment
SUBSCRIPTION_ID = "64e0993d-9026-4add-b0f9-284be5c9fcf3"
RESOURCE_GROUP = "ODL-DataEng-292169"
LOCATION = "westeurope"

# Naming convention: Use your actual first name and last initial
# Example: If name is "John Doe", use "john-d"
STUDENT_SUFFIX = "rodolfo-l"  # UPDATE THIS with your name

# Resource names following Azure naming conventions
STORAGE_ACCOUNT = f"adlsnycpayroll{STUDENT_SUFFIX.replace('-', '')}"  # Must be lowercase, no hyphens
SQL_SERVER_NAME = f"sqlserver-nycpayroll-{STUDENT_SUFFIX}"
SQL_DB_NAME = "db_nycpayroll"
DATA_FACTORY_NAME = f"adf-nycpayroll-{STUDENT_SUFFIX}"
SYNAPSE_WORKSPACE_NAME = f"synapse-nycpayroll-{STUDENT_SUFFIX}"

# SQL Server admin credentials
SQL_ADMIN_USER = "sqladmin"
SQL_ADMIN_PASSWORD = "P@ssw0rd1234!"  # Change this to meet your security requirements

def run_command(command, description):
    """Execute Azure CLI command and handle errors"""
    print(f"\n{'='*70}")
    print(f"STEP: {description}")
    print(f"{'='*70}")
    print(f"Command: {command}\n")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr}")
        return None

def create_storage_account():
    """
    Create Azure Data Lake Storage Gen2
    
    WHY: ADLS Gen2 is a cloud data lake that provides:
    - Hierarchical namespace (file system structure, not just blobs)
    - High performance for big data analytics
    - Fine-grained access control
    - Cost-effective storage for large datasets
    
    For Data Scientists: Think of this as your cloud-based file system
    where raw data files live before processing.
    """
    print("\n" + "="*70)
    print("CREATING AZURE DATA LAKE STORAGE GEN2")
    print("="*70)
    
    # Create storage account with hierarchical namespace enabled
    command = f"""az storage account create \
        --name {STORAGE_ACCOUNT} \
        --resource-group {RESOURCE_GROUP} \
        --location {LOCATION} \
        --sku Standard_LRS \
        --kind StorageV2 \
        --enable-hierarchical-namespace true \
        --output json"""
    
    result = run_command(command, "Create Storage Account with Hierarchical Namespace")
    
    if result:
        print("\nStorage Account Created Successfully!")
        print(f"Name: {STORAGE_ACCOUNT}")
        print("\nWHY THIS MATTERS:")
        print("- Hierarchical namespace allows folder/file structure (like your PC)")
        print("- Standard_LRS = Locally Redundant Storage (3 copies in same datacenter)")
        print("- StorageV2 = Latest generation with all features")
    
    return result

def create_containers():
    """
    Create three directories (containers) in ADLS Gen2:
    1. dirpayrollfiles - For current payroll data (2021)
    2. dirhistoryfiles - For historical payroll data (2020)
    3. dirstaging - For intermediate/staging data during pipeline execution
    
    WHY: Organizing data into logical folders helps:
    - Separate historical vs current data
    - Control access at folder level
    - Track data lineage (where data came from)
    """
    print("\n" + "="*70)
    print("CREATING DATA LAKE DIRECTORIES (CONTAINERS)")
    print("="*70)
    
    containers = [
        ("dirpayrollfiles", "Current payroll data (2021)"),
        ("dirhistoryfiles", "Historical payroll data (2020)"),
        ("dirstaging", "Staging area for pipeline processing")
    ]
    
    for container_name, purpose in containers:
        command = f"""az storage container create \
            --name {container_name} \
            --account-name {STORAGE_ACCOUNT} \
            --auth-mode login \
            --output json"""
        
        result = run_command(command, f"Create container: {container_name}")
        if result:
            print(f"Created: {container_name} - {purpose}")
    
    print("\nWHY THIS MATTERS:")
    print("- Separating historical vs current data prevents accidental overwrites")
    print("- Staging area allows transformations without affecting source data")
    print("- In data pipelines, you always separate Bronze/Silver/Gold layers")

def create_sql_server():
    """
    Create Azure SQL Server (logical server)
    
    WHY: SQL Server is needed for:
    - Storing structured data in tables
    - Fast querying with indexes
    - ACID transactions (Atomicity, Consistency, Isolation, Durability)
    - Integration with reporting tools
    
    For Data Scientists: This is where cleaned, transformed data
    lives for analysis and visualization.
    """
    print("\n" + "="*70)
    print("CREATING AZURE SQL SERVER")
    print("="*70)
    
    command = f"""az sql server create \
        --name {SQL_SERVER_NAME} \
        --resource-group {RESOURCE_GROUP} \
        --location {LOCATION} \
        --admin-user {SQL_ADMIN_USER} \
        --admin-password {SQL_ADMIN_PASSWORD} \
        --output json"""
    
    result = run_command(command, "Create SQL Server")
    
    if result:
        print(f"\nSQL Server Created: {SQL_SERVER_NAME}")
        print(f"Admin User: {SQL_ADMIN_USER}")
        print("\nWHY THIS MATTERS:")
        print("- SQL Server is the 'host' - think of it as the building")
        print("- SQL Databases go inside this server - think of them as apartments")
        print("- Centralized security and management for all databases")
    
    return result

def configure_sql_firewall():
    """
    Configure SQL Server firewall to allow Azure services
    
    WHY: By default, SQL Server blocks all connections.
    We need to allow Azure Data Factory and Synapse to connect.
    """
    print("\n" + "="*70)
    print("CONFIGURING SQL SERVER FIREWALL")
    print("="*70)
    
    # Allow Azure services
    command = f"""az sql server firewall-rule create \
        --server {SQL_SERVER_NAME} \
        --resource-group {RESOURCE_GROUP} \
        --name AllowAzureServices \
        --start-ip-address 0.0.0.0 \
        --end-ip-address 0.0.0.0 \
        --output json"""
    
    result = run_command(command, "Allow Azure Services")
    
    if result:
        print("\nFirewall Configured!")
        print("Azure services (Data Factory, Synapse) can now connect")
    
    return result

def create_sql_database():
    """
    Create SQL Database inside SQL Server
    
    WHY: This is where our payroll tables will be stored:
    - EMP_MD (Employee Master)
    - TITLE_MD (Title Master)
    - AGENCY_MD (Agency Master)
    - NYC_Payroll_2020
    - NYC_Payroll_2021
    - NYC_Payroll_Summary
    
    Basic tier is cost-effective for development/testing.
    """
    print("\n" + "="*70)
    print("CREATING SQL DATABASE")
    print("="*70)
    
    command = f"""az sql db create \
        --server {SQL_SERVER_NAME} \
        --resource-group {RESOURCE_GROUP} \
        --name {SQL_DB_NAME} \
        --service-objective Basic \
        --output json"""
    
    result = run_command(command, "Create SQL Database")
    
    if result:
        print(f"\nDatabase Created: {SQL_DB_NAME}")
        print("Service Tier: Basic (5 DTUs)")
        print("\nWHY THIS MATTERS:")
        print("- Basic tier = $5/month, suitable for dev/test")
        print("- DTU = Database Transaction Unit (compute power)")
        print("- This database will hold 6 tables with payroll data")
    
    return result

def create_data_factory():
    """
    Create Azure Data Factory
    
    WHY: Data Factory is the ETL (Extract, Transform, Load) tool:
    - Extract: Get data from CSV files in Data Lake
    - Transform: Clean, join, aggregate data
    - Load: Write to SQL Database and Synapse
    
    For Data Scientists: Think of this as your automated data pipeline
    that runs on schedule instead of manual Python scripts.
    """
    print("\n" + "="*70)
    print("CREATING AZURE DATA FACTORY")
    print("="*70)
    
    command = f"""az datafactory create \
        --name {DATA_FACTORY_NAME} \
        --resource-group {RESOURCE_GROUP} \
        --location {LOCATION} \
        --output json"""
    
    result = run_command(command, "Create Data Factory")
    
    if result:
        print(f"\nData Factory Created: {DATA_FACTORY_NAME}")
        print("\nWHY THIS MATTERS:")
        print("- Data Factory orchestrates the entire data pipeline")
        print("- No-code/low-code visual interface for building pipelines")
        print("- Can schedule pipelines to run daily/hourly automatically")
        print("- Monitors pipeline execution and handles errors")
    
    return result

def create_synapse_workspace():
    """
    Create Azure Synapse Analytics workspace
    
    WHY: Synapse provides:
    - Serverless SQL pools for querying Data Lake files directly
    - Big data processing without provisioning servers
    - Integration with Power BI for visualization
    - CETAS (Create External Table As Select) for query results
    
    For Data Scientists: This lets you query CSV/Parquet files
    using SQL without loading them into a database first.
    """
    print("\n" + "="*70)
    print("CREATING AZURE SYNAPSE ANALYTICS WORKSPACE")
    print("="*70)
    
    # Synapse needs its own storage account for workspace data
    synapse_storage = f"synapsestorage{STUDENT_SUFFIX.replace('-', '')}"
    
    # Create storage for Synapse
    command = f"""az storage account create \
        --name {synapse_storage} \
        --resource-group {RESOURCE_GROUP} \
        --location {LOCATION} \
        --sku Standard_LRS \
        --kind StorageV2 \
        --enable-hierarchical-namespace true \
        --output json"""
    
    run_command(command, "Create Synapse Storage Account")
    
    # Create file system for Synapse workspace
    command = f"""az storage container create \
        --name workspace \
        --account-name {synapse_storage} \
        --auth-mode login \
        --output json"""
    
    run_command(command, "Create Synapse Workspace Container")
    
    # Create Synapse workspace
    command = f"""az synapse workspace create \
        --name {SYNAPSE_WORKSPACE_NAME} \
        --resource-group {RESOURCE_GROUP} \
        --location {LOCATION} \
        --storage-account {synapse_storage} \
        --file-system workspace \
        --sql-admin-login-user {SQL_ADMIN_USER} \
        --sql-admin-login-password {SQL_ADMIN_PASSWORD} \
        --output json"""
    
    result = run_command(command, "Create Synapse Workspace")
    
    if result:
        print(f"\nSynapse Workspace Created: {SYNAPSE_WORKSPACE_NAME}")
        print("\nWHY THIS MATTERS:")
        print("- Serverless SQL pool = Pay only for queries you run")
        print("- Query Data Lake files directly without copying to database")
        print("- CETAS creates external tables from query results")
        print("- Power BI can connect directly to Synapse for dashboards")
    
    return result

def configure_synapse_firewall():
    """
    Configure Synapse workspace firewall
    """
    print("\n" + "="*70)
    print("CONFIGURING SYNAPSE FIREWALL")
    print("="*70)
    
    command = f"""az synapse firewall-rule create \
        --name AllowAllAzureIPs \
        --workspace-name {SYNAPSE_WORKSPACE_NAME} \
        --resource-group {RESOURCE_GROUP} \
        --start-ip-address 0.0.0.0 \
        --end-ip-address 0.0.0.0 \
        --output json"""
    
    result = run_command(command, "Allow Azure Services to Synapse")
    
    if result:
        print("\nSynapse firewall configured!")
    
    return result

def print_summary():
    """Print summary of all created resources"""
    print("\n" + "="*70)
    print("INFRASTRUCTURE CREATION COMPLETE")
    print("="*70)
    
    print(f"""
RESOURCE SUMMARY:
-----------------
Subscription ID:      {SUBSCRIPTION_ID}
Resource Group:       {RESOURCE_GROUP}
Location:             {LOCATION}

Data Lake Storage:    {STORAGE_ACCOUNT}
  - dirpayrollfiles   (Current data)
  - dirhistoryfiles   (Historical data)
  - dirstaging        (Pipeline staging)

SQL Server:           {SQL_SERVER_NAME}
SQL Database:         {SQL_DB_NAME}
  Admin User:         {SQL_ADMIN_USER}

Data Factory:         {DATA_FACTORY_NAME}

Synapse Workspace:    {SYNAPSE_WORKSPACE_NAME}
  Admin User:         {SQL_ADMIN_USER}

NEXT STEPS:
-----------
1. Upload CSV files to Data Lake using script 02_upload_data.py
2. Create SQL tables using script 03_create_sql_tables.py
3. Create Data Factory pipelines via Azure Portal
4. Create Synapse external table

IMPORTANT NOTES:
----------------
- Save SQL Admin Password securely: {SQL_ADMIN_PASSWORD}
- Storage Account Key will be needed for Synapse external data source
""")

def main():
    """Execute all infrastructure creation steps"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║         NYC PAYROLL DATA ANALYTICS - INFRASTRUCTURE SETUP         ║
    ║                     Azure Data Engineering Project                ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    print("\nThis script will create all required Azure resources.")
    print("Estimated time: 10-15 minutes")
    
    input("\nPress Enter to start...")
    
    # Step 1: Create Storage Account
    if not create_storage_account():
        print("\nFailed to create storage account. Exiting.")
        sys.exit(1)
    
    # Step 2: Create Containers
    create_containers()
    
    # Step 3: Create SQL Server
    if not create_sql_server():
        print("\nFailed to create SQL Server. Exiting.")
        sys.exit(1)
    
    # Step 4: Configure SQL Firewall
    configure_sql_firewall()
    
    # Step 5: Create SQL Database
    create_sql_database()
    
    # Step 6: Create Data Factory
    create_data_factory()
    
    # Step 7: Create Synapse Workspace
    create_synapse_workspace()
    
    # Step 8: Configure Synapse Firewall
    configure_synapse_firewall()
    
    # Print Summary
    print_summary()
    
    print("\n✓ Infrastructure setup complete!")
    print("Check docs/PROJECT_STATUS.md for next steps.")

if __name__ == "__main__":
    main()
