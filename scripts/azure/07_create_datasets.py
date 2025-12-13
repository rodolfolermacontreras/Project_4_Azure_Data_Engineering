"""
Step 3: Create Datasets in Azure Data Factory (Automated)

Datasets define schema/structure of data sources and destinations.
We create 12 datasets total:
- 5 CSV source files from Data Lake
- 6 SQL table destinations
- 1 Synapse external table destination
"""

import subprocess
import json
import os

# Configuration
RESOURCE_GROUP = "ODL-DataEng-292169"
DATA_FACTORY = "adf-nycpayroll-rodolfo-l"
AZ_CLI = r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"

print("=" * 80)
print("STEP 3: Creating Datasets in Azure Data Factory")
print("=" * 80)
print()

# ============================================================================
# CSV DATASETS (5) - Source files from Data Lake
# ============================================================================
print("PART 1: Creating CSV Source Datasets (5)")
print("-" * 80)

csv_datasets = [
    ("ds_AgencyMaster", "dirpayrollfiles", "AgencyMaster.csv"),
    ("ds_EmpMaster", "dirpayrollfiles", "EmpMaster.csv"),
    ("ds_TitleMaster", "dirpayrollfiles", "TitleMaster.csv"),
    ("ds_nycpayroll_2020", "dirhistoryfiles", "nycpayroll_2020.csv"),
    ("ds_nycpayroll_2021", "dirpayrollfiles", "nycpayroll_2021.csv"),
]

for name, container, filename in csv_datasets:
    print(f"Creating: {name}")
    
    dataset = {
        "properties": {
            "linkedServiceName": {
                "referenceName": "ls_AdlsGen2",
                "type": "LinkedServiceReference"
            },
            "type": "DelimitedText",
            "typeProperties": {
                "location": {
                    "type": "AzureBlobFSLocation",
                    "fileName": filename,
                    "folderPath": "",
                    "fileSystem": container
                },
                "columnDelimiter": ",",
                "escapeChar": "\\",
                "firstRowAsHeader": True,
                "quoteChar": "\""
            },
            "schema": []
        }
    }
    
    # Save to temp file
    temp_file = f"temp_{name}.json"
    with open(temp_file, "w") as f:
        json.dump(dataset, f, indent=2)
    
    # Create dataset
    try:
        subprocess.run(
            [AZ_CLI, "datafactory", "dataset", "create",
             "--resource-group", RESOURCE_GROUP,
             "--factory-name", DATA_FACTORY,
             "--name", name,
             "--properties", f"@{temp_file}"],
            check=True, shell=True, capture_output=True, text=True
        )
        print(f"  SUCCESS: {name}")
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: {name}")
        print(f"  {e.stderr}")
    
    os.remove(temp_file)
    print()

print()

# ============================================================================
# SQL TABLE DATASETS (6) - Destination tables in SQL Database
# ============================================================================
print("PART 2: Creating SQL Table Datasets (6)")
print("-" * 80)

sql_datasets = [
    ("ds_NYC_Payroll_AGENCY_MD", "NYC_Payroll_AGENCY_MD"),
    ("ds_NYC_Payroll_EMP_MD", "NYC_Payroll_EMP_MD"),
    ("ds_NYC_Payroll_TITLE_MD", "NYC_Payroll_TITLE_MD"),
    ("ds_NYC_Payroll_Data_2020", "NYC_Payroll_Data_2020"),
    ("ds_NYC_Payroll_Data_2021", "NYC_Payroll_Data_2021"),
    ("ds_NYC_Payroll_Summary", "NYC_Payroll_Summary"),
]

for name, table in sql_datasets:
    print(f"Creating: {name}")
    
    dataset = {
        "properties": {
            "linkedServiceName": {
                "referenceName": "ls_SqlDatabase",
                "type": "LinkedServiceReference"
            },
            "type": "AzureSqlTable",
            "typeProperties": {
                "schema": "dbo",
                "table": table
            },
            "schema": []
        }
    }
    
    # Save to temp file
    temp_file = f"temp_{name}.json"
    with open(temp_file, "w") as f:
        json.dump(dataset, f, indent=2)
    
    # Create dataset
    try:
        subprocess.run(
            [AZ_CLI, "datafactory", "dataset", "create",
             "--resource-group", RESOURCE_GROUP,
             "--factory-name", DATA_FACTORY,
             "--name", name,
             "--properties", f"@{temp_file}"],
            check=True, shell=True, capture_output=True, text=True
        )
        print(f"  SUCCESS: {name}")
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: {name}")
        print(f"  {e.stderr}")
    
    os.remove(temp_file)
    print()

print()

# ============================================================================
# SYNAPSE DATASET (1) - External table in Synapse
# ============================================================================
print("PART 3: Creating Synapse Dataset (1)")
print("-" * 80)

print("Creating: ds_Synapse_NYC_Payroll_Summary")

synapse_dataset = {
    "properties": {
        "linkedServiceName": {
            "referenceName": "ls_Synapse",
            "type": "LinkedServiceReference"
        },
        "type": "AzureSqlDWTable",
        "typeProperties": {
            "schema": "dbo",
            "table": "NYC_Payroll_Summary"
        },
        "schema": []
    }
}

# Save to temp file
temp_file = "temp_ds_Synapse_NYC_Payroll_Summary.json"
with open(temp_file, "w") as f:
    json.dump(synapse_dataset, f, indent=2)

# Create dataset
try:
    subprocess.run(
        [AZ_CLI, "datafactory", "dataset", "create",
         "--resource-group", RESOURCE_GROUP,
         "--factory-name", DATA_FACTORY,
         "--name", "ds_Synapse_NYC_Payroll_Summary",
         "--properties", f"@{temp_file}"],
        check=True, shell=True, capture_output=True, text=True
    )
    print("  SUCCESS: ds_Synapse_NYC_Payroll_Summary")
except subprocess.CalledProcessError as e:
    print("  ERROR: ds_Synapse_NYC_Payroll_Summary")
    print(f"  {e.stderr}")

os.remove(temp_file)
print()

# ============================================================================
# VERIFICATION
# ============================================================================
print("=" * 80)
print("VERIFICATION: Listing all datasets")
print("=" * 80)
print()

result = subprocess.run(
    [AZ_CLI, "datafactory", "dataset", "list",
     "--resource-group", RESOURCE_GROUP,
     "--factory-name", DATA_FACTORY,
     "--query", "[].{Name:name, Type:properties.type}", "-o", "table"],
    capture_output=True, text=True, check=True, shell=True
)

print(result.stdout)

print("=" * 80)
print("STEP 3 COMPLETE!")
print("=" * 80)
print()
print("12 datasets created:")
print("  CSV Source (5): AgencyMaster, EmpMaster, TitleMaster, 2020, 2021")
print("  SQL Tables (6): AGENCY_MD, EMP_MD, TITLE_MD, Data_2020, Data_2021, Summary")
print("  Synapse (1): NYC_Payroll_Summary")
print()
print("Next: Create pipelines with Copy activities and Data Flows")
print()
