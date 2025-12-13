-- =============================================================================
-- NYC Payroll Data Analytics - Synapse Analytics Setup
-- =============================================================================
-- Purpose: Create database, file format, data source, and external table
-- Run this script in Azure Synapse Analytics (Serverless SQL Pool)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Step 1: Create Database (Run this first, then switch to the new database)
-- -----------------------------------------------------------------------------

CREATE DATABASE udacity;
GO

-- IMPORTANT: After running above, refresh the database dropdown and select 'udacity'
-- Then run the remaining scripts below

-- -----------------------------------------------------------------------------
-- Step 2: Create External File Format
-- -----------------------------------------------------------------------------
-- This defines how to read/write CSV files

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

-- -----------------------------------------------------------------------------
-- Step 3: Create External Data Source
-- -----------------------------------------------------------------------------
-- IMPORTANT: Replace the placeholder values with your actual storage account details
-- - Replace 'YOUR_STORAGE_ACCOUNT_NAME' with your ADLS Gen2 storage account name
-- - Replace 'YOUR_CONTAINER_NAME' with your container name
-- - The path should point to dirstaging directory

-- Example: If your storage account is 'adlsnycpayrolljohnw' and container is 'payrollcontainer'
-- The LOCATION would be: 'abfss://payrollcontainer@adlsnycpayrolljohnw.dfs.core.windows.net/dirstaging'

IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE name = 'ExternalDataSourcePayroll')
CREATE EXTERNAL DATA SOURCE [ExternalDataSourcePayroll]
WITH (
    LOCATION = 'abfss://YOUR_CONTAINER_NAME@YOUR_STORAGE_ACCOUNT_NAME.dfs.core.windows.net/dirstaging'
);
GO

-- -----------------------------------------------------------------------------
-- Step 4: Create External Table for Payroll Summary
-- -----------------------------------------------------------------------------
-- This table will be populated by the ADF pipeline via CETAS
-- The table references the dirstaging directory in Data Lake Gen2

CREATE EXTERNAL TABLE [dbo].[NYC_Payroll_Summary](
    [FiscalYear] [int] NULL,
    [AgencyName] [varchar](50) NULL,
    [TotalPaid] [float] NULL
)
WITH (
    LOCATION = '/',
    DATA_SOURCE = [ExternalDataSourcePayroll],
    FILE_FORMAT = [SynapseDelimitedTextFormat]
);
GO

-- =============================================================================
-- Verification Queries
-- =============================================================================

-- Check external file formats
SELECT * FROM sys.external_file_formats;
GO

-- Check external data sources
SELECT * FROM sys.external_data_sources;
GO

-- Check external tables
SELECT * FROM sys.external_tables;
GO

-- Query the external table (run after pipeline execution)
-- SELECT TOP 100 * FROM [dbo].[NYC_Payroll_Summary];
-- GO
