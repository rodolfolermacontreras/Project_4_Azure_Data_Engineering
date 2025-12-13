# Step 4: Create Data Flows in Azure Data Factory (Per Project Requirements)

**PROJECT REQUIREMENT:** Create 5 data flows to load CSV files from Data Lake → SQL Database

---

## Data Flows to Create

Create each data flow in ADF Studio: Author > + > Data flow

### 1. df_Load_AgencyMaster
- Source: ds_AgencyMaster → Sink: ds_NYC_Payroll_AGENCY_MD

### 2. df_Load_EmpMaster
- Source: ds_EmpMaster → Sink: ds_NYC_Payroll_EMP_MD

### 3. df_Load_TitleMaster
- Source: ds_TitleMaster → Sink: ds_NYC_Payroll_TITLE_MD

### 4. df_Load_2020_Payroll
- Source: ds_nycpayroll_2020 → Sink: ds_NYC_Payroll_Data_2020

### 5. df_Load_2021_Payroll
- Source: ds_nycpayroll_2021 → Sink: ds_NYC_Payroll_Data_2021

---

## Step-by-Step Instructions (Repeat 5 times)

### For EACH data flow:

1. ADF Studio > Author > + > Data flow
2. Name: (see list above, e.g., df_Load_AgencyMaster)
3. Click "Add Source"
   - Output stream name: `source`
   - Source type: Dataset
   - Dataset: Select source dataset (e.g., ds_AgencyMaster)
   - Allow schema drift: ✓
4. Click + icon at bottom right of source box > Select "Sink"
   - Output stream name: `sink`
   - Incoming stream: source
   - Sink type: Dataset
   - Dataset: Select sink dataset (e.g., ds_NYC_Payroll_AGENCY_MD)
   - Settings tab:
     - Update method: Allow insert ✓
     - Table action: Recreate table
5. Click "Publish all"

---

## Verification

After creating all 5 data flows, you should see in Author > Data flows:
- df_Load_AgencyMaster
- df_Load_EmpMaster
- df_Load_TitleMaster
- df_Load_2020_Payroll
- df_Load_2021_Payroll

**Screenshots Required:**
- Take screenshot of each data flow showing source → sink connection
- Save configuration files from ADF Studio (export as ARM template)

---

## Why Data Flows Instead of Copy Activity?

Per Udacity requirements, we use data flows to demonstrate ETL capabilities. In production, Copy Activity would be more efficient for simple CSV → Table loads (no transformation needed).

## Pipeline Architecture

We'll create 2 main pipelines:

1. **pl_Load_NYC_Payroll_Data** - Copy CSV files to SQL tables (5 copy activities)
2. **pl_Aggregate_NYC_Payroll_Summary** - Transform and aggregate data to Synapse

---

## PIPELINE 1: Load Data (Copy Activities)

### Purpose
Copy CSV files from Data Lake → SQL Database tables

### Steps in ADF Studio

1. Author > + > Pipeline
2. Name: `pl_Load_NYC_Payroll_Data`
3. Drag **Copy data** activity from Activities pane
4. Repeat 5 times, one for each file

### Copy Activity 1: Agency Master
- Name: `Copy_AgencyMaster`
- Source tab:
  - Source dataset: `ds_AgencyMaster`
- Sink tab:
  - Sink dataset: `ds_NYC_Payroll_AGENCY_MD`
  - Pre-copy script: `TRUNCATE TABLE dbo.NYC_Payroll_AGENCY_MD`

### Copy Activity 2: Employee Master
- Name: `Copy_EmpMaster`
- Source: `ds_EmpMaster`
- Sink: `ds_NYC_Payroll_EMP_MD`
- Pre-copy script: `TRUNCATE TABLE dbo.NYC_Payroll_EMP_MD`

### Copy Activity 3: Title Master
- Name: `Copy_TitleMaster`
- Source: `ds_TitleMaster`
- Sink: `ds_NYC_Payroll_TITLE_MD`
- Pre-copy script: `TRUNCATE TABLE dbo.NYC_Payroll_TITLE_MD`

### Copy Activity 4: 2020 Payroll
- Name: `Copy_2020_Data`
- Source: `ds_nycpayroll_2020`
- Sink: `ds_NYC_Payroll_Data_2020`
- Pre-copy script: `TRUNCATE TABLE dbo.NYC_Payroll_Data_2020`

### Copy Activity 5: 2021 Payroll
- Name: `Copy_2021_Data`
- Source: `ds_nycpayroll_2021`
- Sink: `ds_NYC_Payroll_Data_2021`
- Pre-copy script: `TRUNCATE TABLE dbo.NYC_Payroll_Data_2021`

**Publish all**

### Test the Pipeline
1. Click **Debug** button at top
2. Wait for all 5 activities to complete (green checkmarks)
3. Verify data loaded:

```sql
-- Run in SQL Database Query Editor
SELECT COUNT(*) FROM NYC_Payroll_AGENCY_MD;  -- Should have ~250 rows
SELECT COUNT(*) FROM NYC_Payroll_EMP_MD;     -- Should have ~75k rows
SELECT COUNT(*) FROM NYC_Payroll_TITLE_MD;   -- Should have ~2k rows
SELECT COUNT(*) FROM NYC_Payroll_Data_2020;  -- Should have ~195 rows
SELECT COUNT(*) FROM NYC_Payroll_Data_2021;  -- Should have ~10 rows
```

---

## PIPELINE 2: Aggregate and Load to Synapse

This pipeline will:
1. Union 2020 + 2021 data
2. Join with dimension tables (Agency, Employee, Title)
3. Calculate TotalPaid = RegularGrossPaid + TotalOTPaid + TotalOtherPay
4. Aggregate by FiscalYear + AgencyName
5. Write to Synapse external table (creates CSV in dirstaging)

### Using Data Flow (Visual Transformation)

1. Author > + > Data flow
2. Name: `df_Aggregate_Payroll`

#### Step 1: Add 2020 Source
- Add source > Name: `source2020`
- Source type: Dataset
- Dataset: `ds_NYC_Payroll_Data_2020`

#### Step 2: Add 2021 Source
- Add source > Name: `source2021`
- Source type: Dataset
- Dataset: `ds_NYC_Payroll_Data_2021`

#### Step 3: Union
- Select `source2020` > + > Union
- Union with: `source2021`
- Name: `UnionPayroll`

#### Step 4: Derive TotalPaid Column
- Select `UnionPayroll` > + > Derived Column
- Name: `CalculateTotalPaid`
- Columns:
  - Column name: `TotalPaid`
  - Expression: `RegularGrossPaid + TotalOTPaid + TotalOtherPay`

#### Step 5: Aggregate
- Select `CalculateTotalPaid` > + > Aggregate
- Name: `AggregateByAgency`
- Group by:
  - `FiscalYear`
  - `AgencyName`
- Aggregates:
  - Column name: `TotalPaid`
  - Expression: `sum(TotalPaid)`

#### Step 6: Sink to SQL Summary Table
- Select `AggregateByAgency` > + > Sink
- Name: `SinkToSummary`
- Sink type: Dataset
- Dataset: `ds_NYC_Payroll_Summary`
- Settings:
  - Update method: Allow insert ✓
  - Table action: Truncate table
- Mapping: Auto mapping

#### Step 7: Sink to Synapse (CETAS)
- Go back to `AggregateByAgency` > + > Sink (add another sink)
- Name: `SinkToSynapse`
- Sink type: Dataset
- Dataset: `ds_Synapse_NYC_Payroll_Summary`
- Settings:
  - Update method: Allow insert ✓
  - Table action: Re-create table
- Mapping: Auto mapping

**Publish all**

### Create Pipeline to Execute Data Flow

1. Author > + > Pipeline
2. Name: `pl_Aggregate_NYC_Payroll_Summary`
3. Drag **Data flow** activity from Activities
4. Settings tab:
  - Data flow: `df_Aggregate_Payroll`
  - Compute type: General purpose
  - Core count: 4 (+ Compute optimized)

**Publish all**

### Test the Aggregation Pipeline

1. Click **Debug**
2. Wait for completion (~2-3 minutes for cluster startup)
3. Verify results:

```sql
-- In SQL Database
SELECT * FROM NYC_Payroll_Summary ORDER BY FiscalYear, AgencyName;
-- Should have ~27 rows

-- In Synapse Studio
SELECT * FROM NYC_Payroll_Summary ORDER BY FiscalYear, AgencyName;
-- Should have same 27 rows

-- Check Data Lake
-- Go to dirstaging container - should see NYC_Payroll_Summary.csv
```

Expected total: $36,141,709.69

---

## WHY Data Flow vs Copy Activity?

**Copy Activity:**
- Simple CSV → Table transfer
- No transformation logic
- Fast for large volumes
- Use for: Loading master data

**Data Flow:**
- Visual ETL transformations
- Union, join, aggregate, filter
- Generates Spark code behind scenes
- Use for: Business logic, aggregations

---

## Next Steps

After both pipelines succeed:
1. Take screenshots
2. Create schedule trigger (Step 6)
3. Verify final data
