#!/usr/bin/env python3
"""
Create dataset for Data Lake sink: ds_NYC_Payroll_Summary_DataLake
Points to dirstaging container for CSV output
"""

from azure.identity import AzureCliCredential
from azure.mgmt.datafactory import DataFactoryManagementClient

SUBSCRIPTION_ID = "64e0993d-9026-4add-b0f9-284be5c9fcf3"
RESOURCE_GROUP = "ODL-DataEng-292169"
DATA_FACTORY = "adf-nycpayroll-rodolfo-l"

print("Creating dataset: ds_NYC_Payroll_Summary_DataLake")

credential = AzureCliCredential()
adf_client = DataFactoryManagementClient(credential, SUBSCRIPTION_ID)

dataset_resource = {
    "properties": {
        "linkedServiceName": {
            "referenceName": "ls_AdlsGen2",
            "type": "LinkedServiceReference"
        },
        "type": "DelimitedText",
        "typeProperties": {
            "location": {
                "type": "AzureBlobFSLocation",
                "fileName": "NYC_Payroll_Summary.csv",
                "folderPath": "",
                "fileSystem": "dirstaging"
            },
            "columnDelimiter": ",",
            "escapeChar": "\\",
            "quoteChar": "\"",
            "firstRowAsHeader": True
        },
        "schema": []
    }
}

try:
    adf_client.datasets.create_or_update(
        RESOURCE_GROUP,
        DATA_FACTORY,
        "ds_NYC_Payroll_Summary_DataLake",
        dataset_resource
    )
    print("SUCCESS: ds_NYC_Payroll_Summary_DataLake created")
except Exception as e:
    print(f"ERROR: {str(e)}")
