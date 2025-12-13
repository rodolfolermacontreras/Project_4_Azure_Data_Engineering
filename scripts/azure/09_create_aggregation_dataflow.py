#!/usr/bin/env python3
"""
Step 5: Create Aggregation Data Flow

Creates Dataflow_Summary_Aggregate that:
- Combines 2020 + 2021 payroll data from SQL DB
- Calculates TotalPaid column
- Groups by AgencyName, FiscalYear
- Outputs to SQL DB (NYC_Payroll_Summary) AND Data Lake (dirstaging)
"""

import os
import sys
from azure.identity import AzureCliCredential
from azure.mgmt.datafactory import DataFactoryManagementClient

# Configuration
SUBSCRIPTION_ID = "64e0993d-9026-4add-b0f9-284be5c9fcf3"
RESOURCE_GROUP = "ODL-DataEng-292169"
DATA_FACTORY = "adf-nycpayroll-rodolfo-l"

print("=" * 80)
print("STEP 5: Creating Aggregation Data Flow")
print("=" * 80)
print()

# Authenticate
print("Authenticating...")
credential = AzureCliCredential()
adf_client = DataFactoryManagementClient(credential, SUBSCRIPTION_ID)
print("Authenticated successfully")
print()

# Create aggregation data flow
df_name = "Dataflow_Summary_Aggregate"
print(f"Creating data flow: {df_name}")
print("  - Source 1: 2020 Payroll (SQL)")
print("  - Source 2: 2021 Payroll (SQL)")
print("  - Union both sources")
print("  - Derived Column: TotalPaid = RegularGrossPaid + TotalOTPaid + TotalOtherPay")
print("  - Aggregate: Group by AgencyName, FiscalYear → Sum TotalPaid")
print("  - Sink 1: NYC_Payroll_Summary (SQL DB) - Truncate")
print("  - Sink 2: dirstaging (Data Lake) - Clear folder")
print()

dataflow_resource = {
    "properties": {
        "type": "MappingDataFlow",
        "description": "Aggregate payroll data from 2020 and 2021, calculate total compensation, and output to SQL DB and Data Lake",
        "typeProperties": {
            "sources": [
                {
                    "name": "source2020",
                    "description": "2020 payroll data from SQL DB",
                    "dataset": {
                        "referenceName": "ds_NYC_Payroll_Data_2020",
                        "type": "DatasetReference"
                    }
                },
                {
                    "name": "source2021",
                    "description": "2021 payroll data from SQL DB",
                    "dataset": {
                        "referenceName": "ds_NYC_Payroll_Data_2021",
                        "type": "DatasetReference"
                    }
                }
            ],
            "sinks": [
                {
                    "name": "sinkSQL",
                    "description": "Output to SQL Database summary table",
                    "dataset": {
                        "referenceName": "ds_NYC_Payroll_Summary",
                        "type": "DatasetReference"
                    }
                },
                {
                    "name": "sinkDataLake",
                    "description": "Output to Data Lake staging directory",
                    "dataset": {
                        "referenceName": "ds_NYC_Payroll_Summary_DataLake",
                        "type": "DatasetReference"
                    }
                }
            ],
            "transformations": [
                {
                    "name": "union1",
                    "description": "Combine 2020 and 2021 data"
                },
                {
                    "name": "derivedColumn1",
                    "description": "Calculate TotalPaid"
                },
                {
                    "name": "aggregate1",
                    "description": "Aggregate by Agency and Fiscal Year"
                }
            ],
            "script": """source(output(
        FiscalYear as integer,
        PayrollNumber as integer,
        AgencyID as string,
        AgencyName as string,
        EmployeeID as string,
        LastName as string,
        FirstName as string,
        AgencyStartDate as date,
        WorkLocationBorough as string,
        TitleCode as string,
        TitleDescription as string,
        LeaveStatusasofJune30 as string,
        BaseSalary as double,
        PayBasis as string,
        RegularHours as double,
        RegularGrossPaid as double,
        OTHours as double,
        TotalOTPaid as double,
        TotalOtherPay as double
    ),
    allowSchemaDrift: true,
    validateSchema: false,
    isolationLevel: 'READ_UNCOMMITTED',
    format: 'table') ~> source2020
source(output(
        FiscalYear as integer,
        PayrollNumber as integer,
        AgencyID as string,
        AgencyName as string,
        EmployeeID as string,
        LastName as string,
        FirstName as string,
        AgencyStartDate as date,
        WorkLocationBorough as string,
        TitleCode as string,
        TitleDescription as string,
        LeaveStatusasofJune30 as string,
        BaseSalary as double,
        PayBasis as string,
        RegularHours as double,
        RegularGrossPaid as double,
        OTHours as double,
        TotalOTPaid as double,
        TotalOtherPay as double
    ),
    allowSchemaDrift: true,
    validateSchema: false,
    isolationLevel: 'READ_UNCOMMITTED',
    format: 'table') ~> source2021
source2020, source2021 union(byName: true)~> union1
union1 derive(TotalPaid = RegularGrossPaid + TotalOTPaid + TotalOtherPay) ~> derivedColumn1
derivedColumn1 aggregate(groupBy(AgencyName, FiscalYear),
    TotalPaid = sum(TotalPaid)) ~> aggregate1
aggregate1 sink(allowSchemaDrift: true,
    validateSchema: false,
    input(
        FiscalYear as integer,
        AgencyName as string,
        TotalPaid as double
    ),
    deletable:false,
    insertable:true,
    updateable:false,
    upsertable:false,
    recreate:true,
    format: 'table',
    skipDuplicateMapInputs: true,
    skipDuplicateMapOutputs: true) ~> sinkSQL
aggregate1 sink(allowSchemaDrift: true,
    validateSchema: false,
    truncate: true,
    skipDuplicateMapInputs: true,
    skipDuplicateMapOutputs: true) ~> sinkDataLake"""
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
    print(f"SUCCESS: {df_name} created")
    print()
    print("Data flow includes:")
    print("  ✓ 2 sources (2020 + 2021 payroll from SQL)")
    print("  ✓ Union transformation")
    print("  ✓ Derived column (TotalPaid calculation)")
    print("  ✓ Aggregate (group by AgencyName, FiscalYear)")
    print("  ✓ 2 sinks (SQL DB + Data Lake)")
except Exception as e:
    print(f"ERROR: {df_name}")
    print(f"  {str(e)}")
    sys.exit(1)

print()
print("=" * 80)
print("STEP 5 COMPLETE!")
print("=" * 80)
print()
print("Next: Verify in ADF Studio that Dataflow_Summary_Aggregate exists")
print("      Check that it has 2 sources, transformations, and 2 sinks")
