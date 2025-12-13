# NYC Payroll Data Analytics - Project Status

> Living document tracking all work, decisions, and progress per Udacity project requirements

---

## Current Status (2025-12-13)

| Project Step | Status | Method | Completion Date |
|-------------|--------|--------|-----------------|
| Step 1: Infrastructure Setup | Complete + Screenshots | Automated scripts | 2025-12-13 |
| Step 2: Linked Services (3) | Complete | Manual ADF Studio | 2025-12-13 |
| Step 3: Datasets (12) | Complete | Manual ADF Studio | 2025-12-13 |
| Step 4: Data Flows (5) | Complete + Screenshots | Python SDK (script 08) | 2025-12-13 |
| Step 5: Aggregation Pipeline | Complete + Screenshots | Python SDK (script 09) | 2025-12-13 |
| Step 6: Main Pipeline | Complete | Python SDK (script 10) | 2025-12-13 |
| Step 7: Trigger and Monitor | In Progress - Running | Debug execution | 2025-12-13 |
| Step 7: Verify Data | Not Started | - | - |

---

## PROJECT RECAP: What We've Built

### STEP 1: Infrastructure (COMPLETE)

**Azure Resources Created:**
- Data Lake Gen2: `adlsnycpayrollrodolfol` with 3 containers
  - dirpayrollfiles: 4 CSV files (AgencyMaster, EmpMaster, TitleMaster, nycpayroll_2021)
  - dirhistoryfiles: 1 CSV file (nycpayroll_2020)
  - dirstaging: Empty (for pipeline output)
- SQL Server: `sqlserver-nycpayroll-rodolfo-l.database.windows.net`
- SQL Database: `db_nycpayroll` with 6 tables (all empty, schema only)
  - NYC_Payroll_AGENCY_MD
  - NYC_Payroll_EMP_MD
  - NYC_Payroll_TITLE_MD
  - NYC_Payroll_Data_2020
  - NYC_Payroll_Data_2021
  - NYC_Payroll_Summary
- Data Factory: `adf-nycpayroll-rodolfo-l`
- Synapse Workspace: `synapse-nycpayroll-rodolfo-l`
  - Database: udacity
  - External Table: dbo.NYC_Payroll_Summary (points to dirstaging/NYC_Payroll_Summary.csv - file doesn't exist yet)
  - External File Format: SynapseDelimitedTextFormat (comma-delimited)
  - External Data Source: ExternalDataSourcePayroll

**Scripts Used (Working):**
- 01_create_infrastructure.py - Created all Azure resources
- 02_upload_data.py - Uploaded 8 CSV files to Data Lake
- 03_create_sql_tables.py - Created 6 SQL tables
- 04_create_synapse_external_table.py - Attempted automation (failed, done manually)

**Manual Steps Required:**
- Created Synapse external table via Synapse Studio (sqlcmd limitations)

**Screenshots Taken:** Data Lake with files, SQL tables, Synapse external table

---

### STEP 2: Linked Services (COMPLETE)

**Created 3 Linked Services in ADF Studio:**
1. ls_AdlsGen2 - Connection to Data Lake (account key auth)
2. ls_SqlDatabase - Connection to SQL Database (SQL auth: sqladmin/P@ssw0rd1234!)
3. ls_Synapse - Connection to Synapse serverless SQL (SQL auth: sqladmin/P@ssw0rd1234!)

**Method:** Manual creation in ADF Studio (Azure CLI datafactory extension not working)

**Scripts Attempted (Failed):**
- 06_create_linked_services.py - Abandoned due to CLI extension issues

**Documentation:** STEP2_LINKED_SERVICES.md

---

### STEP 3: Datasets (COMPLETE)

**Created 12 Datasets in ADF Studio:**

**CSV Source Datasets (5):**
1. ds_AgencyMaster - dirpayrollfiles/AgencyMaster.csv
2. ds_EmpMaster - dirpayrollfiles/EmpMaster.csv
3. ds_TitleMaster - dirpayrollfiles/TitleMaster.csv
4. ds_nycpayroll_2020 - dirhistoryfiles/nycpayroll_2020.csv
5. ds_nycpayroll_2021 - dirpayrollfiles/nycpayroll_2021.csv

**SQL Destination Datasets (6):**
6. ds_NYC_Payroll_AGENCY_MD
7. ds_NYC_Payroll_EMP_MD
8. ds_NYC_Payroll_TITLE_MD
9. ds_NYC_Payroll_Data_2020
10. ds_NYC_Payroll_Data_2021
11. ds_NYC_Payroll_Summary

**Synapse Dataset (1):**
12. ds_Synapse_NYC_Payroll_Summary - Empty schema (data doesn't exist yet)

**Method:** Manual creation in ADF Studio (Azure CLI datafactory extension not working)

**Scripts Attempted (Failed):**
- 07_create_datasets.py - Abandoned due to CLI extension issues

**Documentation:** STEP3_DATASETS.md

---

### STEP 4: Data Flows (IN PROGRESS)

**Per Project Requirements:**
Create 5 data flows to load CSV files from Data Lake → SQL Database

**Required Data Flows:**
1. df_Load_AgencyMaster - ds_AgencyMaster → ds_NYC_Payroll_AGENCY_MD
2. df_Load_EmpMaster - ds_EmpMaster → ds_NYC_Payroll_EMP_MD
3. df_Load_TitleMaster - ds_TitleMaster → ds_NYC_Payroll_TITLE_MD
4. df_Load_2020_Payroll - ds_nycpayroll_2020 → ds_NYC_Payroll_Data_2020
5. df_Load_2021_Payroll - ds_nycpayroll_2021 → ds_NYC_Payroll_Data_2021

**Current Method:** Manual creation in ADF Studio
**Reason:** Azure SDK installation blocked in virtual environment, CLI datafactory extension not working

**Script Status:** 
- 08_create_pipelines.py - Abandoned (SDK installation failed)

**Next After Completion:**
- Create 5 data flows manually in ADF Studio per STEP4_PIPELINES.md
- Take screenshots of all 5 data flows
- Export and save configuration files (ARM templates)

---

## Scripts Inventory

### Active Scripts (Keep)
| Script | Purpose | Status |
|--------|---------|--------|
| 01_create_infrastructure.py | Create Azure resources | Complete, working |
| 02_upload_data.py | Upload CSV to Data Lake | Complete, working |
| 03_create_sql_tables.py | Create SQL tables | Complete, working |
| 04_create_synapse_external_table.py | Create Synapse objects | Partial (manual completion needed) |
| 08_create_pipelines.py | Create 5 data flows via Python SDK | Running |

### Deleted Scaffolding Scripts
- 05_fix_synapse_external_table.py - Failed sqlcmd approach
- 06_create_linked_services.py - Failed CLI extension
- 07_create_datasets.py - Failed CLI extension
- 02_create_synapse_objects_configured.sql - Temporary file

---

## Documentation Files

| File | Purpose | Status |
|------|---------|--------|
| PROJECT_STATUS.md | This file - comprehensive tracking | Active |
| OVERVIEW.md | Learning document explaining data engineering concepts | Complete |
| STEP2_LINKED_SERVICES.md | Reference for linked services | Needs cleanup |
| STEP3_DATASETS.md | Reference for datasets | Needs cleanup |
| STEP4_PIPELINES.md | INCORRECT - talks about pipelines not data flows | Delete after Step 4 |

---

## Next Steps (Per Project Instructions)

---

## Work Log

### 2025-12-13 - Azure Infrastructure Creation (Step 1)

**Completed:**
- Logged into Azure with Udacity lab credentials
- Created Azure Data Lake Storage Gen2: `adlsnycpayrollrodolfol`
  - Storage account with hierarchical namespace enabled
  - Created 3 containers:
    - `dirpayrollfiles` - For current payroll data (2021)
    - `dirhistoryfiles` - For historical payroll data (2020)
    - `dirstaging` - For pipeline staging area
- Created Azure SQL Server: `sqlserver-nycpayroll-rodolfo-l.database.windows.net`
  - Configured firewall to allow Azure services
  - Created SQL Database: `db_nycpayroll` (Basic tier, 5 DTUs)
  - SQL Admin User: `sqladmin`
- Created Azure Data Factory: `adf-nycpayroll-rodolfo-l`
- Created Azure Synapse Analytics: `synapse-nycpayroll-rodolfo-l`
  - Created Synapse storage: `synapsestoragerodolfol`
  - Configured firewall rule: AllowAllWindowsAzureIps
  - SQL Admin User: `sqladmin`

**Scripts Created:**
- `scripts/azure/01_create_infrastructure.py` - Automated infrastructure creation with educational explanations
  - Purpose: Create all Azure resources systematically
- `scripts/azure/06_create_linked_services.py` - Attempted automated linked service creation
  - Status: Failed due to datafactory extension installation issues
  - Resolution: Created 3 linked services manually in ADF Studio (ls_AdlsGen2, ls_SqlDatabase, ls_Synapse)
- `scripts/azure/07_create_datasets.py` - Attempted automated dataset creation
  - Purpose: Create 12 datasets (5 CSV, 6 SQL, 1 Synapse)
  - Status: Failed (datafactory CLI extension not working)
  - Resolution: Creating manually in ADF Studio
  
**NOTE:** Scripts 06 and 07 marked for deletion after manual completion (scaffolding only)
  - Will be kept as reference for infrastructure-as-code approach
  - Includes WHY explanations for data scientist learning

**Resources Summary:**
- Subscription: UdacityDS - 195 (64e0993d-9026-4add-b0f9-284be5c9fcf3)
- Resource Group: ODL-DataEng-292169
- Location: West Europe
- Student Suffix: rodolfo-l

**Scripts Created:**
- `scripts/azure/02_upload_data.py` - Upload CSV files to Data Lake
  - Purpose: Automated data ingestion with verification
  - Explains Bronze/Silver/Gold architecture
  - Demonstrates separation of concerns pattern
  - Successfully uploaded 8 files (3 master files to both containers, 2 payroll files to respective containers)

**Data Upload Results:**
- dirpayrollfiles: AgencyMaster.csv, EmpMaster.csv, TitleMaster.csv, nycpayroll_2021.csv (4 files)
- dirhistoryfiles: AgencyMaster.csv, EmpMaster.csv, TitleMaster.csv, nycpayroll_2020.csv (4 files)
- dirstaging: (empty, ready for pipeline use)

**SCREENSHOT REQUIREMENTS:**
- Resource Group overview showing all 5 resources
- Storage Account showing 3 containers with uploaded files
- SQL Database overview
- Data Factory overview
- Synapse workspace overview

**SQL Tables Created:**
- `scripts/azure/03_create_sql_tables.py` - Automated SQL table creation
  - Created 6 tables in db_nycpayroll database
  - Added firewall rule for local IP (76.146.90.11)
  - Tables: AGENCY_MD, EMP_MD, TITLE_MD, Data_2020, Data_2021, Summary

**Synapse External Table Created:**
- `scripts/azure/04_create_synapse_external_table.py` - Synapse setup
  - Created udacity database in Synapse serverless SQL pool
  - Created external file format for CSV parsing
  - Created external data source pointing to dirstaging container
  - Created external table dbo.NYC_Payroll_Summary
  - Added firewall rule for Synapse access

**STEP 1 COMPLETE - READY FOR SCREENSHOTS:**
1. Data Lake: 3 containers with 8 files total
2. SQL Database: 6 tables ready for pipeline data
3. Synapse: External table ready for aggregated results

**Scripts Tracker (Step 1):**
- 01_create_infrastructure.py - Infrastructure automation (KEEP as reference)
- 02_upload_data.py - Data ingestion (KEEP as reference)
- 03_create_sql_tables.py - SQL schema creation (KEEP as reference)
- 04_create_synapse_external_table.py - Synapse setup (KEEP as reference)
- 02_create_synapse_objects_configured.sql - Generated config (Can delete after screenshots)

**Next Steps:**
- Take screenshots per Step 1 requirements
- Create OVERVIEW.md with data engineering concepts explained
- Begin Step 2: Create Linked Services in Data Factory

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
