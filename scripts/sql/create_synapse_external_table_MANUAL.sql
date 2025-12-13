-- =============================================================================
-- Run this script in Synapse Studio Query Editor
-- Make sure to select database: udacity (in the dropdown)
-- =============================================================================

-- Step 1: If database doesn't exist, create it first (run in master database)
-- CREATE DATABASE udacity;
-- GO

-- Step 2: Switch to udacity database in the dropdown, then run below:

-- Create External File Format
IF NOT EXISTS (SELECT * FROM sys.external_file_formats WHERE name = 'SynapseDelimitedTextFormat') 
CREATE EXTERNAL FILE FORMAT [SynapseDelimitedTextFormat] 
WITH (
    FORMAT_TYPE = DELIMITEDTEXT,
    FORMAT_OPTIONS (
        FIELD_TERMINATOR = ',',
        USE_TYPE_DEFAULT = FALSE
    )
);
GO

-- Create External Data Source
IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE name = 'ExternalDataSourcePayroll')
CREATE EXTERNAL DATA SOURCE [ExternalDataSourcePayroll]
WITH (
    LOCATION = 'abfss://dirstaging@adlsnycpayrollrodolfol.dfs.core.windows.net'
);
GO

-- Create External Table
IF NOT EXISTS (SELECT * FROM sys.external_tables WHERE name = 'NYC_Payroll_Summary')
CREATE EXTERNAL TABLE dbo.NYC_Payroll_Summary (
    FiscalYear INT,
    AgencyName VARCHAR(100),
    TotalPaid FLOAT
)
WITH (
    LOCATION = 'NYC_Payroll_Summary.csv',
    DATA_SOURCE = ExternalDataSourcePayroll,
    FILE_FORMAT = SynapseDelimitedTextFormat
);
GO

-- Verify external table was created
SELECT name, type_desc FROM sys.external_tables;
GO
