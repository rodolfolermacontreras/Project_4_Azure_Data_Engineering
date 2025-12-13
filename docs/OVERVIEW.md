# NYC Payroll Data Analytics - Project Overview for Data Scientists

## Purpose of This Document

As a data scientist transitioning to data engineering, this document explains what we built, why each component matters, and how it all connects. Think of this as your bridge from Python/pandas world to cloud data engineering.

---

## Project Goal

**Business Question:** How is NYC allocating its budget? How much goes to salaries vs overtime?

**Technical Goal:** Build an automated data pipeline that:
1. Ingests payroll CSV files from multiple years
2. Cleans and transforms the data
3. Loads it into a database for analysis
4. Creates aggregated summaries for public transparency

**Why This Matters:** In data science, you might run a Jupyter notebook manually. In data engineering, you build **automated, scheduled pipelines** that run without human intervention.

---

## Architecture: From Data Scientist Perspective

### What You Know (Data Science)
```python
# Manual process - you run this yourself
import pandas as pd

# Read data
df_2020 = pd.read_csv('nycpayroll_2020.csv')
df_2021 = pd.read_csv('nycpayroll_2021.csv')

# Rename columns for consistency
df_2021 = df_2021.rename(columns={'AgencyCode': 'AgencyID'})

# Combine
df_union = pd.concat([df_2020, df_2021])

# Aggregate
df_summary = df_union.groupby(['FiscalYear', 'AgencyName'])['TotalPaid'].sum()

# Save
df_summary.to_csv('summary.csv')
```

### What We Built (Data Engineering)
```
Azure Data Lake (CSV files)
    ↓ (Extract - Copy Data)
Azure Data Factory Pipeline
    ↓ (Transform - Clean, Join, Aggregate)
Azure SQL Database (Structured tables)
    ↓ (Load - CETAS)
Azure Synapse (External table for querying)
```

**Key Difference:** This runs **automatically** on a schedule, handles errors, logs execution, scales to terabytes of data, and provides SQL access for analysts who don't code.

---

## Components We Built (Step 1)

### 1. Azure Data Lake Storage Gen2 (ADLS Gen2)

**What Is It:** Cloud file storage with folder structure (like OneDrive, but for big data)

**Data Scientist Analogy:** 
- Your laptop: `C:\data\payroll\` folders
- ADLS Gen2: Cloud version with unlimited storage

**Why We Need It:**
- **Separation of Storage and Compute:** Data lives in cheap storage, processing happens elsewhere
- **Raw Data Preservation:** Keep original CSVs unchanged (reproducibility)
- **Data Lineage:** Track where data came from (historical vs current)

**What We Created:**
- Storage Account: `adlsnycpayrollrodolfol`
- 3 Containers (folders):
  - `dirpayrollfiles` - Current year data (2021)
  - `dirhistoryfiles` - Historical data (2020)
  - `dirstaging` - Intermediate processed data

**Bronze/Silver/Gold Architecture:**
- Bronze = Raw files in Data Lake (what we uploaded)
- Silver = Cleaned data in SQL Database (pipeline will create)
- Gold = Aggregated summaries (final output for users)

---

### 2. Azure SQL Database

**What Is It:** Managed PostgreSQL-like database in the cloud

**Data Scientist Analogy:**
- Your laptop: SQLite database or local PostgreSQL
- Azure SQL DB: Same thing, but managed by Microsoft (no server maintenance)

**Why We Need It:**
- **Structured Storage:** Tables with schemas enforce data quality
- **Fast Queries:** Indexes enable sub-second queries on millions of rows
- **ACID Transactions:** Data integrity guaranteed (no partial updates)
- **SQL Interface:** Analysts can query without Python

**What We Created:**
- Server: `sqlserver-nycpayroll-rodolfo-l.database.windows.net`
- Database: `db_nycpayroll`
- 6 Tables:
  - **Dimension Tables (Master Data):**
    - `NYC_Payroll_AGENCY_MD` - Agency reference data
    - `NYC_Payroll_EMP_MD` - Employee reference data
    - `NYC_Payroll_TITLE_MD` - Job title reference data
  - **Fact Tables (Transactions):**
    - `NYC_Payroll_Data_2020` - Historical payroll records
    - `NYC_Payroll_Data_2021` - Current payroll records
  - **Summary Table (Aggregated):**
    - `NYC_Payroll_Summary` - Pre-calculated totals by agency/year

**Star Schema Design:**
```
       AGENCY_MD
           |
           |
    ┌──────┴──────┐
    |             |
EMP_MD ← NYC_Payroll_2020 → TITLE_MD
         (Fact Table)
    |             |
    └──────┬──────┘
           |
       AGENCY_MD
```

This design enables efficient joins and fast queries.

---

### 3. Azure Data Factory (ADF)

**What Is It:** Cloud-based ETL (Extract, Transform, Load) orchestration tool

**Data Scientist Analogy:**
- Your laptop: Python script with pandas transformations
- ADF: Visual pipeline builder that runs on schedule, no code

**Why We Need It:**
- **Automation:** Run pipelines on schedule (daily, hourly)
- **Orchestration:** Coordinate multiple steps (copy, transform, load)
- **Error Handling:** Retry failed steps, send alerts
- **Scalability:** Process gigabytes in parallel
- **Monitoring:** Track pipeline runs, debug failures

**What We'll Build (Steps 2-6):**
- Linked Services - Connections to Data Lake, SQL DB, Synapse
- Datasets - Schema definitions for CSV files and tables
- Data Flows - Transformations (rename columns, aggregate)
- Pipelines - Orchestrate the entire ETL process

**Pipeline Steps (Preview):**
1. Copy data from CSV → SQL tables (populate master data and payroll)
2. Union 2020 + 2021 data (handle column name differences)
3. Join with dimension tables (add agency names)
4. Aggregate by FiscalYear + AgencyName
5. Write results to Synapse external table

---

### 4. Azure Synapse Analytics

**What Is It:** Serverless SQL engine for querying Data Lake files

**Data Scientist Analogy:**
- Your laptop: `df = pd.read_csv('large_file.csv')` loads into memory
- Synapse: Query CSV without loading into memory, pay per query

**Why We Need It:**
- **Query Data in Place:** No need to copy files to database
- **Serverless:** No servers to manage, pay only for queries
- **CETAS:** Create External Table As Select (write query results as files)
- **Cost-Effective:** Cheaper than provisioning dedicated database

**What We Created:**
- Workspace: `synapse-nycpayroll-rodolfo-l`
- Database: `udacity`
- External Table: `dbo.NYC_Payroll_Summary`
  - Metadata stored in Synapse
  - Data lives in `dirstaging/NYC_Payroll_Summary.csv`
  - Currently empty (pipeline will populate)

**External Table vs Regular Table:**
- Regular Table: Data stored inside database (takes up space)
- External Table: Metadata only, reads files from Data Lake (no storage cost)

---

## Data Engineering Concepts Explained

### 1. Separation of Storage and Compute

**Old Way (Monolithic):**
- Database stores data AND processes queries
- Scaling is expensive (must upgrade entire database)

**Modern Way (Decoupled):**
- Data Lake stores data (cheap)
- Multiple compute engines query it (SQL, Spark, Python)
- Scale storage and compute independently

**Our Implementation:**
- Storage: ADLS Gen2 (pennies per GB)
- Compute: SQL Database for queries, Data Factory for ETL, Synapse for ad-hoc analysis

---

### 2. ETL vs ELT

**ETL (Extract, Transform, Load):**
- Transform data BEFORE loading to database
- Used when target system has limited compute

**ELT (Extract, Load, Transform):**
- Load raw data first, transform INSIDE database
- Used with powerful databases like Synapse

**Our Project Uses Both:**
- ETL: Copy CSV → SQL with light transformations (rename columns)
- ELT: Heavy aggregations happen in SQL (group by, sum)

---

### 3. Data Lineage and Reproducibility

**Why It Matters:**
- Regulations require knowing where data came from
- Debugging requires tracing data through pipeline
- Reproducibility ensures same inputs = same outputs

**How We Implement:**
- Raw CSV files preserved in Data Lake (never modified)
- Each transformation logged in Data Factory
- Separate folders for historical vs current (timestamps implicit)

---

### 4. Schema-on-Write vs Schema-on-Read

**Schema-on-Write (SQL Database):**
- Define table structure BEFORE inserting data
- Enforces data quality (wrong types rejected)
- Example: `FiscalYear INT NOT NULL`

**Schema-on-Read (Data Lake):**
- Store any file format (CSV, JSON, Parquet)
- Define structure WHEN reading (flexible)
- Example: External table reads CSV, infers types

**Our Project:**
- Data Lake: Schema-on-read (CSVs stored as-is)
- SQL Database: Schema-on-write (tables enforce types)
- Synapse: Schema-on-read (external table maps to CSV)

---

### 5. Idempotency in Pipelines

**What Is It:** Running pipeline multiple times produces same result

**Why It Matters:**
- Pipelines fail and need re-runs
- Scheduled runs might overlap
- Data quality depends on consistency

**How We'll Implement:**
- Use `TRUNCATE` before loading data (clear old data)
- Or use `MERGE` to upsert (update if exists, insert if new)
- Prevents duplicate records

---

## Data Flow: End-to-End Journey

### Current State (Step 1 Complete)
```
CSV Files (local) 
    → Uploaded to Data Lake (dirpayrollfiles, dirhistoryfiles)
    → SQL Tables created (empty, awaiting pipeline)
    → Synapse External Table created (awaiting data file)
```

### Future State (After Steps 2-6)
```
1. Scheduled Trigger (Daily 2 AM)
    ↓
2. ADF Pipeline Starts
    ↓
3. Copy Activities:
   - AgencyMaster.csv → NYC_Payroll_AGENCY_MD table
   - EmpMaster.csv → NYC_Payroll_EMP_MD table
   - TitleMaster.csv → NYC_Payroll_TITLE_MD table
   - nycpayroll_2020.csv → NYC_Payroll_Data_2020 table
   - nycpayroll_2021.csv → NYC_Payroll_Data_2021 table
    ↓
4. Data Flow (Transformation):
   - Union 2020 + 2021 (rename AgencyCode → AgencyID)
   - Filter bad fiscal years (1998, 1999)
   - Calculate TotalPaid = RegularGrossPaid + TotalOTPaid + TotalOtherPay
   - Aggregate: GROUP BY FiscalYear, AgencyName SUM(TotalPaid)
    ↓
5. Load to Synapse:
   - CETAS writes NYC_Payroll_Summary.csv to dirstaging
   - External table now queryable
    ↓
6. Verification:
   - Query SQL tables (should have 195 rows in 2020, 10 in 2021)
   - Query Synapse external table (should have 27 summary rows)
   - Total salary = $36,141,709.69
    ↓
7. Monitoring:
   - Data Factory logs execution time, row counts
   - Alerts on failure
   - Dashboard shows pipeline health
```

---

## Key Differences: Data Science vs Data Engineering

| Aspect | Data Science | Data Engineering |
|--------|--------------|------------------|
| **Focus** | Insights, models, predictions | Pipelines, infrastructure, automation |
| **Tools** | Jupyter, pandas, scikit-learn | Data Factory, SQL, orchestration tools |
| **Scale** | Sample data, local processing | Full datasets, distributed processing |
| **Execution** | Manual, ad-hoc | Automated, scheduled |
| **Output** | Jupyter notebook, visualization | Production database, API endpoints |
| **Error Handling** | Re-run cell | Retry logic, alerting, logging |
| **Users** | Yourself, team | Entire organization, external users |
| **Latency** | Minutes to hours | Seconds to minutes (real-time) |

---

## What We Learned (Technical Skills)

### Azure Services
- **ADLS Gen2:** Hierarchical namespace, container structure
- **SQL Database:** Tables, schemas, DTUs, firewall rules
- **Data Factory:** Linked services, datasets, pipelines (coming in Steps 2-6)
- **Synapse:** External tables, CETAS, serverless SQL pools

### Data Engineering Patterns
- **Bronze/Silver/Gold:** Raw → Cleaned → Aggregated
- **Star Schema:** Fact tables + dimension tables
- **External Tables:** Query files without copying
- **Separation of Concerns:** Storage vs compute, historical vs current

### SQL Concepts
- **DDL (Data Definition Language):** CREATE TABLE, CREATE DATABASE
- **Primary Keys:** Unique identifiers for rows
- **Foreign Keys:** References between tables
- **External Data Sources:** Metadata pointing to files

### Cloud Concepts
- **Managed Services:** Microsoft handles servers, backups, patching
- **Pay-per-Use:** Synapse charges per TB scanned, not per hour
- **Firewall Rules:** Control who can access resources
- **Resource Groups:** Logical containers for related resources

---

## Next Steps (Steps 2-6)

### Step 2: Create Linked Services
**What:** Define connections to Data Lake, SQL DB, Synapse  
**Why:** Data Factory needs credentials to access resources  
**Analogy:** Like `pd.read_csv('path')` but for cloud resources

### Step 3: Create Datasets
**What:** Define schema for CSV files and SQL tables  
**Why:** Tell Data Factory what columns exist, their types  
**Analogy:** Like pandas DataFrame column dtypes

### Step 4: Create Data Flows
**What:** Visual transformations (rename, join, aggregate)  
**Why:** Business logic for cleaning and aggregating data  
**Analogy:** Like pandas operations (merge, groupby, sum)

### Step 5: Create Pipelines
**What:** Orchestrate copy activities + data flows  
**Why:** Coordinate entire ETL process  
**Analogy:** Like a Python script with multiple steps

### Step 6: Trigger and Monitor
**What:** Schedule pipeline runs, check logs  
**Why:** Ensure pipeline runs successfully every day  
**Analogy:** Like cron job + logging

---

## Big Picture: Why This Architecture?

### Scalability
- Data Lake: Handles petabytes
- Data Factory: Processes in parallel
- SQL Database: Indexes for fast queries

### Cost Efficiency
- Store data cheap (Data Lake: $0.02/GB)
- Process only when needed (Synapse: pay per query)
- No idle servers (serverless everything)

### Reliability
- Multiple copies of data (geo-redundant)
- Automatic retries on failure
- Monitoring and alerting

### Accessibility
- SQL interface for analysts
- Power BI for dashboards
- API endpoints for applications

### Governance
- Access control (who can read what)
- Audit logs (who accessed when)
- Data lineage (where data came from)

---

## Key Takeaways

1. **Cloud data engineering** automates what data scientists do manually
2. **Separation of storage and compute** enables scalability and cost savings
3. **Pipelines replace notebooks** for production workloads
4. **SQL databases** provide structured access for non-Python users
5. **External tables** enable querying files without copying data
6. **Star schema** organizes data for efficient queries
7. **Automation and monitoring** ensure reliability

---

## Resources Tracker

### Scripts Created (Keep)
- `01_create_infrastructure.py` - Infrastructure automation
- `02_upload_data.py` - Data ingestion
- `03_create_sql_tables.py` - SQL schema creation
- `04_create_synapse_external_table.py` - Synapse setup

### Scripts Created (Can Delete After Project)
- `05_fix_synapse_external_table.py` - Troubleshooting script
- `02_create_synapse_objects_configured.sql` - Generated config

### Documentation
- `README.md` - Project overview
- `PROJECT_STATUS.md` - Work log and progress
- `OVERVIEW.md` - This document (learning guide)

---

## Glossary for Data Scientists

- **ADLS Gen2:** Azure Data Lake Storage Generation 2
- **ADF:** Azure Data Factory
- **CETAS:** Create External Table As Select
- **DTU:** Database Transaction Unit (compute power)
- **ETL:** Extract, Transform, Load
- **HDFS:** Hadoop Distributed File System (inspiration for ADLS Gen2)
- **Linked Service:** Connection configuration in ADF
- **Serverless:** No servers to manage, pay per use
- **Star Schema:** Fact tables surrounded by dimension tables
- **Synapse:** Azure's analytics platform (SQL + Spark)

---

*Last Updated: 2025-12-13*  
*Project: NYC Payroll Data Analytics*  
*Author: Rodolfo Lerma*
