"""
Step 2: Create Linked Services in Azure Data Factory

Linked Services = Connection configurations to external resources
Think of these as connection strings with credentials

We create 3 linked services:
1. ADLS Gen2 (Data Lake) - Read CSV files
2. Azure SQL Database - Write to tables
3. Synapse workspace - Write to external tables
"""

import subprocess
import json
import os

# Configuration
RESOURCE_GROUP = "ODL-DataEng-292169"
DATA_FACTORY = "adf-nycpayroll-rodolfo-l"
STORAGE_ACCOUNT = "adlsnycpayrollrodolfol"
SQL_SERVER = "sqlserver-nycpayroll-rodolfo-l"
SQL_DATABASE = "db_nycpayroll"
SQL_ADMIN_USER = "sqladmin"
SQL_ADMIN_PASSWORD = "P@ssw0rd1234!"
SYNAPSE_WORKSPACE = "synapse-nycpayroll-rodolfo-l"

# Azure CLI path
AZ_CLI = r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"

# Get subscription ID
result = subprocess.run(
    [AZ_CLI, "account", "show", "--query", "id", "-o", "tsv"],
    capture_output=True, text=True, check=True, shell=True
)
SUBSCRIPTION_ID = result.stdout.strip()

print("=" * 80)
print("STEP 2: Creating Linked Services in Azure Data Factory")
print("=" * 80)
print()

# ============================================================================
# 1. ADLS Gen2 Linked Service
# ============================================================================
print("1. Creating ADLS Gen2 Linked Service...")
print("   WHY: Allows ADF to read CSV files from Data Lake")
print("   AUTH: Uses storage account key for simplicity")
print()

# Get storage account key
result = subprocess.run(
    [AZ_CLI, "storage", "account", "keys", "list",
     "--resource-group", RESOURCE_GROUP,
     "--account-name", STORAGE_ACCOUNT,
     "--query", "[0].value", "-o", "tsv"],
    capture_output=True, text=True, check=True, shell=True
)
storage_key = result.stdout.strip()

adls_linked_service = {
    "name": "ls_AdlsGen2",
    "properties": {
        "type": "AzureBlobFS",
        "typeProperties": {
            "url": f"https://{STORAGE_ACCOUNT}.dfs.core.windows.net",
            "accountKey": {
                "type": "SecureString",
                "value": storage_key
            }
        }
    }
}

# Save to temp file
with open("temp_adls_ls.json", "w") as f:
    json.dump(adls_linked_service, f, indent=2)

# Create linked service
subprocess.run(
    [AZ_CLI, "datafactory", "linked-service", "create",
     "--resource-group", RESOURCE_GROUP,
     "--factory-name", DATA_FACTORY,
     "--name", "ls_AdlsGen2",
     "--properties", "@temp_adls_ls.json"],
    check=True, shell=True
)

os.remove("temp_adls_ls.json")
print("   ✓ ADLS Gen2 Linked Service created: ls_AdlsGen2")
print()

# ============================================================================
# 2. Azure SQL Database Linked Service (Legacy)
# ============================================================================
print("2. Creating Azure SQL Database Linked Service (Legacy)...")
print("   WHY: Allows ADF to write data to SQL tables")
print("   NOTE: Using Legacy type per project requirements")
print("   AUTH: SQL authentication with username/password")
print()

sql_linked_service = {
    "name": "ls_SqlDatabase",
    "properties": {
        "type": "AzureSqlDatabase",
        "typeProperties": {
            "connectionString": f"Server=tcp:{SQL_SERVER}.database.windows.net,1433;Database={SQL_DATABASE};User ID={SQL_ADMIN_USER};Password={SQL_ADMIN_PASSWORD};Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
        }
    }
}

# Save to temp file
with open("temp_sql_ls.json", "w") as f:
    json.dump(sql_linked_service, f, indent=2)

# Create linked service
subprocess.run(
    [AZ_CLI, "datafactory", "linked-service", "create",
     "--resource-group", RESOURCE_GROUP,
     "--factory-name", DATA_FACTORY,
     "--name", "ls_SqlDatabase",
     "--properties", "@temp_sql_ls.json"],
    check=True, shell=True
)

os.remove("temp_sql_ls.json")
print("   ✓ Azure SQL Database Linked Service created: ls_SqlDatabase")
print()

# ============================================================================
# 3. Synapse Linked Service
# ============================================================================
print("3. Creating Synapse Linked Service...")
print("   WHY: Allows ADF to execute CETAS (Create External Table As Select)")
print("   AUTH: Managed Identity (ADF automatically authenticates)")
print()

synapse_linked_service = {
    "name": "ls_Synapse",
    "properties": {
        "type": "AzureSqlDW",
        "typeProperties": {
            "connectionString": f"Server=tcp:{SYNAPSE_WORKSPACE}-ondemand.sql.azuresynapse.net,1433;Database=udacity;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
        }
    }
}

# Save to temp file
with open("temp_synapse_ls.json", "w") as f:
    json.dump(synapse_linked_service, f, indent=2)

# Create linked service
subprocess.run(
    [AZ_CLI, "datafactory", "linked-service", "create",
     "--resource-group", RESOURCE_GROUP,
     "--factory-name", DATA_FACTORY,
     "--name", "ls_Synapse",
     "--properties", "@temp_synapse_ls.json"],
    check=True, shell=True
)

os.remove("temp_synapse_ls.json")
print("   ✓ Synapse Linked Service created: ls_Synapse")
print()

# ============================================================================
# Verification
# ============================================================================
print("=" * 80)
print("VERIFICATION: Listing all linked services")
print("=" * 80)
print()

result = subprocess.run(
    [AZ_CLI, "datafactory", "linked-service", "list",
     "--resource-group", RESOURCE_GROUP,
     "--factory-name", DATA_FACTORY,
     "--query", "[].{Name:name, Type:properties.type}", "-o", "table"],
    capture_output=True, text=True, check=True, shell=True
)

print(result.stdout)

print("=" * 80)
print("STEP 2 COMPLETE!")
print("=" * 80)
print()
print("Next Steps:")
print("1. Take screenshot of linked services in Data Factory Studio")
print("2. Run script 07_create_datasets.py to create datasets")
print()
print("DATA ENGINEERING CONCEPT:")
print("-" * 80)
print("Linked Services vs Datasets:")
print("  • Linked Service = WHERE the data is (connection config)")
print("  • Dataset = WHAT the data looks like (schema definition)")
print()
print("Analogy:")
print("  • Linked Service = Database connection string")
print("  • Dataset = Table name + column definitions")
print()
