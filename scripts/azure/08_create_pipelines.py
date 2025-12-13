"""
Step 4: Create Data Flows using Azure Data Factory Python SDK

Per project requirements:
Create 5 separate data flows, one for each CSV file → SQL table
- df_Load_AgencyMaster
- df_Load_EmpMaster
- df_Load_TitleMaster
- df_Load_2020_Payroll
- df_Load_2021_Payroll

Each data flow: Source (CSV dataset) → Sink (SQL table)
"""

from azure.identity import AzureCliCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *
import time

# Configuration
SUBSCRIPTION_ID = "64e0993d-9026-4add-b0f9-284be5c9fcf3"
RESOURCE_GROUP = "ODL-DataEng-292169"
DATA_FACTORY = "adf-nycpayroll-rodolfo-l"

print("=" * 80)
print("STEP 4: Creating 5 Data Flows (per project requirements)")
print("=" * 80)
print()

# Authenticate
print("Authenticating...")
credential = AzureCliCredential()
adf_client = DataFactoryManagementClient(credential, SUBSCRIPTION_ID)
print("Authenticated successfully")
print()

# ============================================================================
# CREATE 5 DATA FLOWS (one for each CSV → SQL table load)
# ============================================================================

dataflow_configs = [
    ("df_Load_AgencyMaster", "ds_AgencyMaster", "ds_NYC_Payroll_AGENCY_MD", "Agency master data"),
    ("df_Load_EmpMaster", "ds_EmpMaster", "ds_NYC_Payroll_EMP_MD", "Employee master data"),
    ("df_Load_TitleMaster", "ds_TitleMaster", "ds_NYC_Payroll_TITLE_MD", "Title master data"),
    ("df_Load_2020_Payroll", "ds_nycpayroll_2020", "ds_NYC_Payroll_Data_2020", "2020 payroll data"),
    ("df_Load_2021_Payroll", "ds_nycpayroll_2021", "ds_NYC_Payroll_Data_2021", "2021 payroll data"),
]

for df_name, source_ds, sink_ds, description in dataflow_configs:
    print(f"Creating data flow: {df_name}")
    print(f"  Source: {source_ds} → Sink: {sink_ds}")
    
    # Create data flow resource with properties wrapper
    dataflow_resource = {
        "properties": {
            "type": "MappingDataFlow",
            "description": f"Load {description} from Data Lake to SQL Database",
            "typeProperties": {
                "sources": [
                    {
                        "name": "source",
                        "dataset": {
                            "referenceName": source_ds,
                            "type": "DatasetReference"
                        }
                    }
                ],
                "sinks": [
                    {
                        "name": "sink",
                        "dataset": {
                            "referenceName": sink_ds,
                            "type": "DatasetReference"
                        }
                    }
                ],
                "script": f"source(allowSchemaDrift: true, validateSchema: false) ~> source\nsource sink(allowSchemaDrift: true, validateSchema: false, deletable:false, insertable:true, updateable:false, upsertable:false, recreate:true, format: 'table', skipDuplicateMapInputs: true, skipDuplicateMapOutputs: true) ~> sink"
            }
        }
    }
    
    try:
        adf_client.data_flows.create_or_update(
            RESOURCE_GROUP,
            DATA_FACTORY,
            df_name,
            dataflow_resource
        )
        print(f"  SUCCESS: {df_name} created")
    except Exception as e:
        print(f"  ERROR: {df_name}")
        print(f"  {str(e)}")
    
    print()

print("=" * 80)
print("STEP 4 COMPLETE!")
print("=" * 80)
print()
print("5 data flows created:")
for df_name, _, _, _ in dataflow_configs:
    print(f"  - {df_name}")
print()
print("Next: Verify data flows in ADF Studio and take screenshots")
