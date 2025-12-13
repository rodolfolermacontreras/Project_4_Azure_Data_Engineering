#!/usr/bin/env python3
"""
Step 6: Create Main Pipeline

Creates pipeline that orchestrates all data flows:
1. Parallel: Load master data (Agency, Employee, Title)
2. Sequential: Load 2020 payroll → Load 2021 payroll
3. Final: Run aggregation (after all loads complete)
"""

import sys
from azure.identity import AzureCliCredential
from azure.mgmt.datafactory import DataFactoryManagementClient

# Configuration
SUBSCRIPTION_ID = "64e0993d-9026-4add-b0f9-284be5c9fcf3"
RESOURCE_GROUP = "ODL-DataEng-292169"
DATA_FACTORY = "adf-nycpayroll-rodolfo-l"

print("=" * 80)
print("STEP 6: Creating Main Pipeline")
print("=" * 80)
print()

# Authenticate
print("Authenticating...")
credential = AzureCliCredential()
adf_client = DataFactoryManagementClient(credential, SUBSCRIPTION_ID)
print("Authenticated successfully")
print()

pipeline_name = "pl_NYC_Payroll_Pipeline"
print(f"Creating pipeline: {pipeline_name}")
print()
print("Pipeline structure:")
print("  1. Parallel execution:")
print("     - df_Load_AgencyMaster")
print("     - df_Load_EmpMaster")
print("     - df_Load_TitleMaster")
print("  2. Sequential execution (after master data):")
print("     - df_Load_2020_Payroll")
print("     - df_Load_2021_Payroll")
print("  3. Final aggregation (after all loads):")
print("     - Dataflow_Summary_Aggregate")
print()

# Pipeline definition
pipeline_resource = {
    "properties": {
        "activities": [
            # Activity 1: Load Agency Master
            {
                "name": "Load_AgencyMaster",
                "type": "ExecuteDataFlow",
                "dependsOn": [],
                "policy": {
                    "timeout": "0.12:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": False,
                    "secureInput": False
                },
                "typeProperties": {
                    "dataFlow": {
                        "referenceName": "df_Load_AgencyMaster",
                        "type": "DataFlowReference"
                    },
                    "compute": {
                        "coreCount": 8,
                        "computeType": "General"
                    },
                    "traceLevel": "Fine"
                }
            },
            # Activity 2: Load Employee Master
            {
                "name": "Load_EmpMaster",
                "type": "ExecuteDataFlow",
                "dependsOn": [],
                "policy": {
                    "timeout": "0.12:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": False,
                    "secureInput": False
                },
                "typeProperties": {
                    "dataFlow": {
                        "referenceName": "df_Load_EmpMaster",
                        "type": "DataFlowReference"
                    },
                    "compute": {
                        "coreCount": 8,
                        "computeType": "General"
                    },
                    "traceLevel": "Fine"
                }
            },
            # Activity 3: Load Title Master
            {
                "name": "Load_TitleMaster",
                "type": "ExecuteDataFlow",
                "dependsOn": [],
                "policy": {
                    "timeout": "0.12:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": False,
                    "secureInput": False
                },
                "typeProperties": {
                    "dataFlow": {
                        "referenceName": "df_Load_TitleMaster",
                        "type": "DataFlowReference"
                    },
                    "compute": {
                        "coreCount": 8,
                        "computeType": "General"
                    },
                    "traceLevel": "Fine"
                }
            },
            # Activity 4: Load 2020 Payroll (depends on all 3 master loads)
            {
                "name": "Load_2020_Payroll",
                "type": "ExecuteDataFlow",
                "dependsOn": [
                    {
                        "activity": "Load_AgencyMaster",
                        "dependencyConditions": ["Succeeded"]
                    },
                    {
                        "activity": "Load_EmpMaster",
                        "dependencyConditions": ["Succeeded"]
                    },
                    {
                        "activity": "Load_TitleMaster",
                        "dependencyConditions": ["Succeeded"]
                    }
                ],
                "policy": {
                    "timeout": "0.12:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": False,
                    "secureInput": False
                },
                "typeProperties": {
                    "dataFlow": {
                        "referenceName": "df_Load_2020_Payroll",
                        "type": "DataFlowReference"
                    },
                    "compute": {
                        "coreCount": 8,
                        "computeType": "General"
                    },
                    "traceLevel": "Fine"
                }
            },
            # Activity 5: Load 2021 Payroll (depends on 2020 completion)
            {
                "name": "Load_2021_Payroll",
                "type": "ExecuteDataFlow",
                "dependsOn": [
                    {
                        "activity": "Load_2020_Payroll",
                        "dependencyConditions": ["Succeeded"]
                    }
                ],
                "policy": {
                    "timeout": "0.12:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": False,
                    "secureInput": False
                },
                "typeProperties": {
                    "dataFlow": {
                        "referenceName": "df_Load_2021_Payroll",
                        "type": "DataFlowReference"
                    },
                    "compute": {
                        "coreCount": 8,
                        "computeType": "General"
                    },
                    "traceLevel": "Fine"
                }
            },
            # Activity 6: Aggregate (depends on 2021 completion)
            {
                "name": "Aggregate_Payroll_Summary",
                "type": "ExecuteDataFlow",
                "dependsOn": [
                    {
                        "activity": "Load_2021_Payroll",
                        "dependencyConditions": ["Succeeded"]
                    }
                ],
                "policy": {
                    "timeout": "0.12:00:00",
                    "retry": 0,
                    "retryIntervalInSeconds": 30,
                    "secureOutput": False,
                    "secureInput": False
                },
                "typeProperties": {
                    "dataFlow": {
                        "referenceName": "Dataflow_Summary_Aggregate",
                        "type": "DataFlowReference"
                    },
                    "compute": {
                        "coreCount": 8,
                        "computeType": "General"
                    },
                    "traceLevel": "Fine"
                }
            }
        ],
        "annotations": []
    }
}

try:
    adf_client.pipelines.create_or_update(
        RESOURCE_GROUP,
        DATA_FACTORY,
        pipeline_name,
        pipeline_resource
    )
    print(f"SUCCESS: {pipeline_name} created")
    print()
    print("Pipeline includes 6 activities:")
    print("  ✓ Load_AgencyMaster (parallel)")
    print("  ✓ Load_EmpMaster (parallel)")
    print("  ✓ Load_TitleMaster (parallel)")
    print("  ✓ Load_2020_Payroll (after master data)")
    print("  ✓ Load_2021_Payroll (after 2020)")
    print("  ✓ Aggregate_Payroll_Summary (after all loads)")
except Exception as e:
    print(f"ERROR: {pipeline_name}")
    print(f"  {str(e)}")
    sys.exit(1)

print()
print("=" * 80)
print("STEP 6 COMPLETE!")
print("=" * 80)
print()
print("Next Steps:")
print("  1. Open ADF Studio → Author → Pipelines")
print("  2. Open pl_NYC_Payroll_Pipeline")
print("  3. Take screenshot showing all 6 activities")
print("  4. Click 'Debug' to test run the pipeline")
print("  5. Monitor execution in Monitor tab")
