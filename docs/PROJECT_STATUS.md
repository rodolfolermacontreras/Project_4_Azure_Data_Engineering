# NYC Payroll Data Analytics - Project Status

> This is the living document for tracking all project work, decisions, and progress.

---

## Current Status

| Item | Status | Last Updated |
|------|--------|--------------|
| Project Setup | Completed | 2024-12-06 |
| Step 1: Data Infrastructure | Not Started | - |
| Step 2: Linked Services | Not Started | - |
| Step 3: Datasets | Not Started | - |
| Step 4: Data Flows | Not Started | - |
| Step 5: Aggregation/Parameterization | Not Started | - |
| Step 6: Pipeline Creation | Not Started | - |
| Step 7: Trigger and Monitor | Not Started | - |
| Step 8: Verify Artifacts | Not Started | - |
| Step 9: GitHub Connection | Not Started | - |

---

## Work Log

### 2024-12-06 - Project Initialization

**Completed:**
- Created project folder structure:
  - `config/` - Configuration files
  - `data/` - Local data samples (all 5 CSV files present)
  - `docs/` - Documentation
  - `notebooks/` - Jupyter notebooks
  - `pipelines/` - ADF pipeline definitions
  - `scripts/` - Utility scripts
  - `scripts/sql/` - SQL scripts for database setup
- Created `README.md` with project overview
- Created `PROJECT_STATUS.md` (this document)
- Set up Python virtual environment (.venv)
- Created SQL scripts:
  - `01_create_sqldb_tables.sql` - All 6 SQL DB tables
  - `02_create_synapse_objects.sql` - Synapse database, file format, data source, external table
  - `03_verification_queries.sql` - Queries to verify pipeline execution

**Data Files Verified:**
- `data/AgencyMaster.csv` - Agency master data
- `data/EmpMaster.csv` - Employee master data
- `data/TitleMaster.csv` - Title master data
- `data/nycpayroll_2020.csv` - Historical payroll (goes to dirhistoryfiles)
- `data/nycpayroll_2021.csv` - Current payroll (goes to dirpayrollfiles)

**Decisions Made:**
- Using Python virtual environment for all local development
- All documentation updates will be tracked in this file
- Scaffolding scripts will be tracked and cleaned up after integration
- SQL scripts organized in `scripts/sql/` folder

**Next Steps:**
- Create Azure resources (Step 1)
- Upload data files to Data Lake

### 2024-12-06 - Data Exploration

**Completed:**
- Created Jupyter notebook `notebooks/01_data_exploration.ipynb`
- Analyzed all 5 CSV data files

**Data File Summary:**

| File | Rows | Columns | Key Column |
|------|------|---------|------------|
| AgencyMaster.csv | 153 | 2 | AgencyID |
| EmpMaster.csv | 1,000 | 3 | EmployeeID |
| TitleMaster.csv | 1,446 | 2 | TitleCode |
| nycpayroll_2020.csv | 100 | 19 | - |
| nycpayroll_2021.csv | 101 | 19 | - |

**Key Findings:**

1. **Critical Column Difference:**
   - 2020 payroll uses column: `AgencyID`
   - 2021 payroll uses column: `AgencyCode`
   - **Action Required:** In ADF Union transformation, map AgencyCode to AgencyID

2. **Data Quality:**
   - No null values in payroll data
   - No duplicate keys in master data
   - 1 null value in TitleMaster.TitleDescription (row unknown)

3. **Data Quality Issue - Fiscal Years:**
   - 2020 file: 1 record with FiscalYear=1998 (EmployeeID: 15188, Agency: OFFICE OF MANAGEMENT & BUDGET)
   - 2021 file: 1 record with FiscalYear=1999 (EmployeeID: 229552, Agency: POLICE DEPARTMENT)
   - **Note:** These are likely test data or data entry errors. The fiscal year filter parameter in the pipeline will handle this.

4. **Salary Statistics:**
   - 2020 Total Paid: $7,011,499.14
   - 2021 Total Paid: $29,130,210.55
   - Combined Total: $36,141,709.69

5. **Categorical Values:**
   - Leave Status: ACTIVE, CEASED, ON SEPARATION LEAVE
   - Pay Basis: per Annum, per Day, per Hour
   - Boroughs: MANHATTAN, BROOKLYN, QUEENS, BRONX, RICHMOND, OTHER

6. **Expected Output:**
   - After aggregation: 27 summary records (by AgencyName + FiscalYear)

**Decisions Made:**
- Created exploration notebook for future reference and validation
- Fiscal year filter parameter will exclude records with unexpected years

**Next Steps:**
- Begin Azure infrastructure setup (Step 1)

---

## Scripts Tracker

| Script | Location | Purpose | Status | Integration Target |
|--------|----------|---------|--------|-------------------|
| 01_data_exploration.ipynb | notebooks/ | Data exploration and validation | Active | Reference/Validation |
| 01_create_sqldb_tables.sql | scripts/sql/ | Create 6 tables in SQL DB | Active | Run in Azure SQL DB |
| 02_create_synapse_objects.sql | scripts/sql/ | Create Synapse DB, file format, external table | Active | Run in Synapse |
| 03_verification_queries.sql | scripts/sql/ | Verify data after pipeline runs | Active | Run in SQL DB and Synapse |

**Status Legend:**
- `Active` - Currently in use
- `Scaffolding` - Temporary, to be integrated
- `Integrated` - Code merged into main pipeline
- `Deprecated` - Marked for deletion

---

## Screenshots Checklist

All screenshots should be saved in `docs/screenshots/` folder.

### Step 1: Data Infrastructure
- [ ] `step1_datalake_files.png` - DataLake Gen2 showing uploaded files in dirpayrollfiles
- [ ] `step1_datalake_history.png` - DataLake Gen2 showing nycpayroll_2020.csv in dirhistoryfiles
- [ ] `step1_sqldb_tables.png` - All 6 tables created in SQL DB
- [ ] `step1_synapse_external_table.png` - External table created in Synapse

### Step 2: Linked Services
- [ ] `step2_linked_services.png` - Linked Services page after creation

### Step 3: Datasets
- [ ] `step3_datasets.png` - All datasets in Data Factory

### Step 4: Data Flows
- [ ] `step4_dataflows.png` - All dataflows in Data Factory

### Step 5: Aggregation
- [ ] `step5_aggregate_dataflow.png` - Aggregate dataflow in Data Factory

### Step 6-8: Pipeline
- [ ] `step6_pipeline.png` - Pipeline resource from Data Factory
- [ ] `step7_pipeline_run_success.png` - Successful pipeline run with all activities
- [ ] `step8_sqldb_summary_query.png` - Query from SQL DB summary table
- [ ] `step8_dirstaging_files.png` - dirstaging directory listing in Datalake
- [ ] `step8_synapse_query.png` - Query from Synapse external table

---

## Azure Resources

| Resource | Naming Convention | Status | Notes |
|----------|-------------------|--------|-------|
| Resource Group | (provided by Udacity) | Not Created | Use provided RG |
| Storage Account (ADLS Gen2) | adlsnycpayroll-[firstname]-[lastinitial] | Not Created | Enable hierarchical namespace |
| SQL Database | db_nycpayroll | Not Created | Service tier: Basic |
| SQL Server | (created with SQL DB) | Not Created | Allow Azure services access |
| Data Factory | (your choice) | Not Created | For pipeline orchestration |
| Synapse Analytics | (your choice or existing) | Not Created | Only 1 allowed per account |
| Synapse SQL Pool | Built-in serverless | Not Created | Use CETAS for external tables |

### ADLS Gen2 Directory Structure

```
storage-container/
|-- dirpayrollfiles/        <- Upload: EmpMaster.csv, AgencyMaster.csv, TitleMaster.csv, nycpayroll_2021.csv
|-- dirhistoryfiles/        <- Upload: nycpayroll_2020.csv
|-- dirstaging/             <- Pipeline output for Synapse external table
```

### SQL Database Tables (6 total)

| Table | Purpose |
|-------|---------|
| NYC_Payroll_EMP_MD | Employee master data |
| NYC_Payroll_TITLE_MD | Job title master data |
| NYC_Payroll_AGENCY_MD | Agency master data |
| NYC_Payroll_Data_2020 | Historical payroll transactions |
| NYC_Payroll_Data_2021 | Current payroll transactions |
| NYC_Payroll_Summary | Aggregated summary (destination) |

---

## Data Pipeline Architecture

```
                    +------------------+
                    |  ADLS Gen2       |
                    |  (Source)        |
                    +--------+---------+
                             |
        +--------------------+--------------------+
        |                    |                    |
        v                    v                    v
+---------------+   +---------------+   +---------------+
| dirpayrollfiles|   | dirhistoryfiles|   | dirstaging   |
| - EmpMaster   |   | - nycpayroll  |   | (output)     |
| - AgencyMaster|   |   _2020.csv   |   |              |
| - TitleMaster |   +---------------+   +---------------+
| - nycpayroll  |           |                    ^
|   _2021.csv   |           |                    |
+-------+-------+           |                    |
        |                   |                    |
        +-------------------+                    |
                  |                              |
                  v                              |
        +------------------+                     |
        |  Azure SQL DB    |                     |
        |  (Staging)       |                     |
        |  - 3 Master tbls |                     |
        |  - 2 Payroll tbls|                     |
        |  - 1 Summary tbl +---------------------+
        +--------+---------+
                 |
                 v
        +------------------+
        |  Synapse Analytics|
        |  (External Table) |
        |  - NYC_Payroll_   |
        |    Summary        |
        +------------------+
```

---

## Data Flow Specifications

### Individual Load Flows (5 total)
| Flow Name | Source (ADLS Gen2) | Destination (SQL DB) |
|-----------|-------------------|---------------------|
| df_load_emp | EmpMaster.csv | NYC_Payroll_EMP_MD |
| df_load_title | TitleMaster.csv | NYC_Payroll_TITLE_MD |
| df_load_agency | AgencyMaster.csv | NYC_Payroll_AGENCY_MD |
| df_load_payroll_2020 | nycpayroll_2020.csv | NYC_Payroll_Data_2020 |
| df_load_payroll_2021 | nycpayroll_2021.csv | NYC_Payroll_Data_2021 |

### Aggregation Flow
| Flow Name | Sources | Transformations | Destinations |
|-----------|---------|-----------------|--------------|
| Dataflow_Summary | NYC_Payroll_Data_2020 (SQL), NYC_Payroll_Data_2021 (SQL) | Union, Filter (FiscalYear param), Derived Column (TotalPaid), Aggregate (by AgencyName, FiscalYear) | 1. NYC_Payroll_Summary (SQL), 2. dirstaging (ADLS Gen2) |

**TotalPaid Formula:** `RegularGrossPaid + TotalOTPaid + TotalOtherPay`

**Important Mapping Note:** 
- 2020 data uses `AgencyID`
- 2021 data uses `AgencyCode`
- Map AgencyCode to AgencyID in the union

---

## Pipeline Flow

```
[Agency Flow] ----+
                  |
[Employee Flow]---+---> Wait ---> [Payroll 2020 Flow] ---+
                  |                                       |
[Title Flow] -----+               [Payroll 2021 Flow] ---+---> [Aggregate Flow]
                                                                    |
                                                                    v
                                                        +-------------------+
                                                        | Sink 1: SQL DB    |
                                                        | Sink 2: dirstaging|
                                                        +-------------------+
```

---

## Global Parameters

| Parameter | Type | Default | Purpose |
|-----------|------|---------|---------|
| dataflow_param_fiscalyear | int | 2020 | Filter fiscal year in aggregation |

---

## Data Pipeline Checklist

### Step 1: Prepare Data Infrastructure
- [ ] Create Azure Data Lake Storage Gen2
  - [ ] Enable hierarchical namespace (Advanced tab)
  - [ ] Enable secure transfer for REST API
  - [ ] Allow anonymous access on containers
  - [ ] Enable storage account key access
  - [ ] Default to Microsoft Entra authorization
- [ ] Create storage container
- [ ] Create directories: dirpayrollfiles, dirhistoryfiles, dirstaging
- [ ] Upload files to dirpayrollfiles: EmpMaster.csv, AgencyMaster.csv, TitleMaster.csv, nycpayroll_2021.csv
- [ ] Upload files to dirhistoryfiles: nycpayroll_2020.csv
- [ ] Create Azure Data Factory
- [ ] Create SQL Database (db_nycpayroll)
  - [ ] Service tier: Basic
  - [ ] Allow Azure services access
  - [ ] Add current client IP to firewall
- [ ] Run SQL script to create 6 tables
- [ ] Create Synapse Analytics workspace (or use existing)
- [ ] Create database 'udacity' in Synapse
- [ ] Create external file format, data source, external table

### Step 2: Create Linked Services
- [ ] Create Linked Service to Azure Data Lake Gen2
- [ ] Test connection
- [ ] Create Linked Service to SQL Database
  - [ ] Set Version to "Legacy" (important!)
- [ ] Test connection

### Step 3: Create Datasets
- [ ] Create dataset for nycpayroll_2021.csv (DelimitedText)
- [ ] Create dataset for EmpMaster.csv
- [ ] Create dataset for TitleMaster.csv
- [ ] Create dataset for AgencyMaster.csv
- [ ] Create dataset for nycpayroll_2020.csv
- [ ] Create datasets for all 6 SQL DB tables
- [ ] Create dataset for Synapse NYC_Payroll_Summary
- [ ] Publish all datasets

### Step 4: Create Data Flows
- [ ] Create data flow: Load 2020 Payroll (ADLS to SQL)
- [ ] Create data flow: Load 2021 Payroll (ADLS to SQL)
- [ ] Create data flow: Load Employee Master
- [ ] Create data flow: Load Title Master
- [ ] Create data flow: Load Agency Master

### Step 5: Aggregation and Parameterization
- [ ] Create Dataflow_Summary
- [ ] Add source: Payroll 2020 from SQL DB
- [ ] Add source: Payroll 2021 from SQL DB
- [ ] Add Select activity (for column mapping if needed)
- [ ] Add Union activity
- [ ] Add Filter activity with parameter (dataflow_param_fiscalyear)
- [ ] Add Derived Column: TotalPaid = RegularGrossPaid + TotalOTPaid + TotalOtherPay
- [ ] Add Aggregate: Group by AgencyName, FiscalYear; Sum TotalPaid
- [ ] Add Sink 1: NYC_Payroll_Summary (SQL DB) with Truncate
- [ ] Add Sink 2: dirstaging (ADLS Gen2) with Clear folder

### Step 6: Pipeline Creation
- [ ] Create main pipeline
- [ ] Add parallel: Agency, Employee, Title dataflows
- [ ] Add sequential: Payroll 2020, Payroll 2021 (after master data)
- [ ] Add Aggregate dataflow (after payroll flows)
- [ ] Create global parameter for fiscal year

### Step 7: Trigger and Monitor
- [ ] Trigger pipeline
- [ ] Monitor execution
- [ ] Verify all activities succeed

### Step 8: Verify Artifacts
- [ ] Query SQL DB summary table
- [ ] Check dirstaging directory for files
- [ ] Query Synapse external table

### Step 9: GitHub Connection
- [ ] Create GitHub repository
- [ ] Connect Azure Data Factory to GitHub
- [ ] Publish all objects to repository

---

## Issues and Blockers

| Issue | Description | Status | Resolution |
|-------|-------------|--------|------------|
| (none yet) | - | - | - |

---

## Known Issues and Solutions (from project instructions)

| Issue | Solution |
|-------|----------|
| ADLS Gen2 linked service error: 'EndpointUnsupportedAccountFeatures' | Delete storage, recreate with hierarchical namespace enabled in Advanced tab |
| SQL linked service: MissingRequiredPropertyException | Set Version to "Legacy" in linked service |
| Column not found: FiscalYear in dataset | Import schema in dataset settings |
| AgencyID not found in 2021 payroll | Map from AgencyCode column instead |
| Cannot create dedicated SQL pool in Synapse | Use serverless SQL pool with CETAS (CREATE EXTERNAL TABLE AS SELECT) |

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2024-12-06 | Initial project setup | Project kickoff |
| 2024-12-06 | Created SQL scripts for DB and Synapse setup | Streamline Azure resource creation |
| 2024-12-06 | Added complete project checklist and specifications | Full requirements documentation |

---

## Project Plan

### High-Level Milestones

1. **Project Setup** (Completed - 2024-12-06)
   - Create folder structure
   - Set up development environment
   - Document project requirements
   - Create SQL scripts

2. **Step 1: Data Infrastructure Setup**
   - Create ADLS Gen2 with directories
   - Upload CSV files
   - Create Azure Data Factory
   - Create SQL Database and tables
   - Create Synapse workspace and external table

3. **Step 2: Create Linked Services**
   - Link to ADLS Gen2
   - Link to SQL Database (Version: Legacy)

4. **Step 3: Create Datasets**
   - Source datasets (CSV files)
   - Destination datasets (SQL tables)
   - Synapse dataset

5. **Step 4: Create Data Flows**
   - 5 individual load flows (ADLS to SQL)

6. **Step 5: Aggregation and Parameterization**
   - Create Dataflow_Summary with:
     - Union, Filter, Derived Column, Aggregate
     - Two sinks (SQL DB and dirstaging)
   - Add fiscal year parameter

7. **Step 6: Pipeline Creation**
   - Orchestrate all dataflows
   - Parallel execution of master data flows
   - Sequential execution of payroll and aggregation

8. **Step 7-8: Testing and Verification**
   - Trigger pipeline
   - Monitor execution
   - Verify data in all destinations

9. **Step 9: GitHub Integration**
   - Connect ADF to GitHub
   - Publish all objects
   - Submit repository

---

## Rubric Requirements Summary

| Category | Requirements |
|----------|-------------|
| Linked Services | 1x AzureBlobFS (ADLS Gen2), 1x AzureSQLDatabase |
| Datasets | Multiple AzureBlobFSLocation (5 CSVs), Multiple AzureSqlTable (6 tables) |
| Data Flows | MappingDataFlow with union, derived column (TotalPaid), aggregate |
| Pipeline | ExecuteDataFlow activities, successful execution screenshot |
| Verification | Screenshots: Gen2 storage data, SQL DB query, Synapse query |

---

## References

- [Azure Data Factory Documentation](https://docs.microsoft.com/en-us/azure/data-factory/)
- [Azure Synapse Analytics Documentation](https://docs.microsoft.com/en-us/azure/synapse-analytics/)
- [Azure Data Lake Storage Gen2](https://docs.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)
- [CETAS in Synapse](https://docs.microsoft.com/en-us/azure/synapse-analytics/sql/develop-tables-cetas)
