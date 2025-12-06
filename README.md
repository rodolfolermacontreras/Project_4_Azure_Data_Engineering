# NYC Payroll Data Analytics Platform

## Project Overview

This project develops a Data Analytics platform on Azure Synapse Analytics for the City of New York with two primary objectives:

1. **Budget Analysis**: Analyze how the City's financial resources are allocated and how much of the City's budget is being devoted to overtime.
2. **Public Transparency**: Make the data available to the interested public to show how the City's budget is being spent on salary and overtime pay for all municipal employees.

## Architecture

The solution implements an end-to-end data pipeline using Azure services:

```
DataLake Gen2 (Source) --> Azure SQL DB (Staging) --> DataLake Gen2 (Target) --> Synapse Analytics
                                    ^
                                    |
                            Azure Data Factory
                            (Orchestration)
```

### Components

| Component | Purpose |
|-----------|---------|
| Azure Data Lake Gen2 | Source storage for CSV files and target storage for aggregated data |
| Azure SQL Database | Staging area with data views |
| Azure Data Factory | Pipeline orchestration and data transformation |
| Azure Synapse Analytics | Analytics platform with external tables for reporting |

## Data Model

### Source Datasets (CSV files in Data Lake)

| Dataset | Description |
|---------|-------------|
| NYC_Payroll_AGENCY_MD | Agency master data (AgencyID, AgencyName) |
| NYC_Payroll_EMP_MD | Employee master data (EmployeeID, LastName, FirstName) |
| NYC_Payroll_TITLE_MD | Title master data (TitleCode, TitleDescription) |
| NYC_Payroll_Data | Monthly payroll transaction data |

### Entity Relationships

- `NYC_Payroll_AGENCY_MD` --> `NYC_Payroll_Data` (via AgencyID)
- `NYC_Payroll_EMP_MD` --> `NYC_Payroll_Data` (via EmployeeID)
- `NYC_Payroll_TITLE_MD` --> `NYC_Payroll_Data` (via TitleCode)

## Folder Structure

```
Project4/
|-- config/              # Configuration files (connection strings, parameters)
|-- data/                # Source CSV data files
|   |-- AgencyMaster.csv
|   |-- EmpMaster.csv
|   |-- TitleMaster.csv
|   |-- nycpayroll_2020.csv
|   |-- nycpayroll_2021.csv
|-- docs/                # Project documentation
|   |-- PROJECT_STATUS.md    # Living document with progress tracking
|   |-- screenshots/         # Screenshots for submission
|-- notebooks/           # Jupyter notebooks for exploration
|-- pipelines/           # ADF pipeline definitions (synced from GitHub)
|-- scripts/             # Utility scripts
|   |-- sql/             # SQL scripts for database setup
|       |-- 01_create_sqldb_tables.sql
|       |-- 02_create_synapse_objects.sql
|       |-- 03_verification_queries.sql
|-- .venv/               # Python virtual environment
|-- .gitignore           # Git ignore file
|-- README.md            # This file
```

## Getting Started

### Prerequisites

- Azure Subscription with the following resources:
  - Azure Data Lake Gen2 Storage Account
  - Azure SQL Database
  - Azure Data Factory
  - Azure Synapse Analytics Workspace
- Python 3.x with virtual environment
- Azure CLI installed and configured

### Local Development Setup

```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies (when requirements.txt is available)
pip install -r requirements.txt
```

## Documentation

See the `docs/` folder for detailed documentation:

- `PROJECT_STATUS.md` - Live project status, updates, work in progress, and complete checklist

## SQL Scripts

Located in `scripts/sql/`:

| Script | Purpose |
|--------|---------|
| `01_create_sqldb_tables.sql` | Create all 6 tables in Azure SQL Database |
| `02_create_synapse_objects.sql` | Create Synapse database, file format, data source, external table |
| `03_verification_queries.sql` | Queries to verify data after pipeline execution |

## Project Steps

1. **Step 1**: Prepare Data Infrastructure (ADLS Gen2, SQL DB, Data Factory, Synapse)
2. **Step 2**: Create Linked Services (ADLS Gen2, SQL Database)
3. **Step 3**: Create Datasets (CSV files, SQL tables, Synapse table)
4. **Step 4**: Create Data Flows (5 load flows for master and payroll data)
5. **Step 5**: Create Aggregation Flow with parameterization
6. **Step 6**: Create Pipeline to orchestrate all flows
7. **Step 7**: Trigger and Monitor Pipeline
8. **Step 8**: Verify Pipeline artifacts
9. **Step 9**: Connect to GitHub

## Development Rules

1. Always use the virtual environment (.venv) for Python operations
2. Document all changes in PROJECT_STATUS.md with dates and reasoning
3. Track all scripts - no orphan code allowed
4. Scaffolding scripts must be integrated or removed after testing
5. Keep documentation updated as work progresses

## License

This project is developed for the Udacity Azure Data Engineering Nanodegree.
