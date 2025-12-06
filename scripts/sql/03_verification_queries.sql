-- =============================================================================
-- NYC Payroll Data Analytics - Verification Queries
-- =============================================================================
-- Purpose: Queries to verify data after pipeline execution
-- =============================================================================

-- -----------------------------------------------------------------------------
-- SQL Database Verification Queries
-- Run these in Azure SQL Database (db_nycpayroll)
-- -----------------------------------------------------------------------------

-- Check row counts for all tables
SELECT 'NYC_Payroll_EMP_MD' AS TableName, COUNT(*) AS RowCount FROM [dbo].[NYC_Payroll_EMP_MD]
UNION ALL
SELECT 'NYC_Payroll_TITLE_MD', COUNT(*) FROM [dbo].[NYC_Payroll_TITLE_MD]
UNION ALL
SELECT 'NYC_Payroll_AGENCY_MD', COUNT(*) FROM [dbo].[NYC_Payroll_AGENCY_MD]
UNION ALL
SELECT 'NYC_Payroll_Data_2020', COUNT(*) FROM [dbo].[NYC_Payroll_Data_2020]
UNION ALL
SELECT 'NYC_Payroll_Data_2021', COUNT(*) FROM [dbo].[NYC_Payroll_Data_2021]
UNION ALL
SELECT 'NYC_Payroll_Summary', COUNT(*) FROM [dbo].[NYC_Payroll_Summary];
GO

-- Sample data from Employee Master
SELECT TOP 10 * FROM [dbo].[NYC_Payroll_EMP_MD];
GO

-- Sample data from Title Master
SELECT TOP 10 * FROM [dbo].[NYC_Payroll_TITLE_MD];
GO

-- Sample data from Agency Master
SELECT TOP 10 * FROM [dbo].[NYC_Payroll_AGENCY_MD];
GO

-- Sample data from 2020 Payroll
SELECT TOP 10 * FROM [dbo].[NYC_Payroll_Data_2020];
GO

-- Sample data from 2021 Payroll
SELECT TOP 10 * FROM [dbo].[NYC_Payroll_Data_2021];
GO

-- Query Summary Table (Destination) - Run after pipeline execution
SELECT 
    FiscalYear,
    AgencyName,
    TotalPaid
FROM [dbo].[NYC_Payroll_Summary]
ORDER BY FiscalYear, TotalPaid DESC;
GO

-- Summary statistics
SELECT 
    FiscalYear,
    COUNT(*) AS AgencyCount,
    SUM(TotalPaid) AS GrandTotalPaid,
    AVG(TotalPaid) AS AvgTotalPaid
FROM [dbo].[NYC_Payroll_Summary]
GROUP BY FiscalYear
ORDER BY FiscalYear;
GO

-- -----------------------------------------------------------------------------
-- Synapse Analytics Verification Queries
-- Run these in Synapse Analytics (udacity database)
-- -----------------------------------------------------------------------------

-- Query external table
SELECT TOP 100 * FROM [dbo].[NYC_Payroll_Summary];
GO

-- Summary by Fiscal Year
SELECT 
    FiscalYear,
    COUNT(*) AS AgencyCount,
    SUM(TotalPaid) AS GrandTotalPaid
FROM [dbo].[NYC_Payroll_Summary]
GROUP BY FiscalYear
ORDER BY FiscalYear;
GO
