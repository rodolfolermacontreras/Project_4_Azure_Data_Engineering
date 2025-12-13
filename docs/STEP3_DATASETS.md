# Step 3: Create 12 Datasets in ADF Studio

## PART 1: CSV Datasets (5)

### ds_AgencyMaster
1. ADF Studio > Author > + next to Datasets
2. Select: **Azure Data Lake Storage Gen2** > Continue
3. Select: **DelimitedText** > Continue
4. Name: `ds_AgencyMaster`
5. Linked service: `ls_AdlsGen2`
6. File path: Click Browse > Select `dirpayrollfiles` > Select `AgencyMaster.csv`
7. First row as header: **Check the box**
8. Import schema: **From connection/store**
9. OK

### ds_EmpMaster
1. + next to Datasets > Azure Data Lake Storage Gen2 > DelimitedText > Continue
2. Name: `ds_EmpMaster`
3. Linked service: `ls_AdlsGen2`
4. File path: Browse > `dirpayrollfiles` > `EmpMaster.csv`
5. First row as header: **✓**
6. Import schema: From connection/store
7. OK

### ds_TitleMaster
1. + next to Datasets > Azure Data Lake Storage Gen2 > DelimitedText > Continue
2. Name: `ds_TitleMaster`
3. Linked service: `ls_AdlsGen2`
4. File path: Browse > `dirpayrollfiles` > `TitleMaster.csv`
5. First row as header: **✓**
6. Import schema: From connection/store
7. OK

### ds_nycpayroll_2020
1. + next to Datasets > Azure Data Lake Storage Gen2 > DelimitedText > Continue
2. Name: `ds_nycpayroll_2020`
3. Linked service: `ls_AdlsGen2`
4. File path: Browse > `dirhistoryfiles` > `nycpayroll_2020.csv`
5. First row as header: **✓**
6. Import schema: From connection/store
7. OK

### ds_nycpayroll_2021
1. + next to Datasets > Azure Data Lake Storage Gen2 > DelimitedText > Continue
2. Name: `ds_nycpayroll_2021`
3. Linked service: `ls_AdlsGen2`
4. File path: Browse > `dirpayrollfiles` > `nycpayroll_2021.csv`
5. First row as header: **✓**
6. Import schema: From connection/store
7. OK

**Click "Publish all" button at top**

---

## PART 2: SQL Datasets (6)

### ds_NYC_Payroll_AGENCY_MD
1. + next to Datasets > **Azure SQL Database** > Continue
2. Name: `ds_NYC_Payroll_AGENCY_MD`
3. Linked service: `ls_SqlDatabase`
4. Table name: Click dropdown > Select `dbo.NYC_Payroll_AGENCY_MD`
5. Import schema: From connection/store
6. OK

### ds_NYC_Payroll_EMP_MD
1. + > Azure SQL Database > Continue
2. Name: `ds_NYC_Payroll_EMP_MD`
3. Linked service: `ls_SqlDatabase`
4. Table: `dbo.NYC_Payroll_EMP_MD`
5. Import schema: From connection/store
6. OK

### ds_NYC_Payroll_TITLE_MD
1. + > Azure SQL Database > Continue
2. Name: `ds_NYC_Payroll_TITLE_MD`
3. Linked service: `ls_SqlDatabase`
4. Table: `dbo.NYC_Payroll_TITLE_MD`
5. Import schema: From connection/store
6. OK

### ds_NYC_Payroll_Data_2020
1. + > Azure SQL Database > Continue
2. Name: `ds_NYC_Payroll_Data_2020`
3. Linked service: `ls_SqlDatabase`
4. Table: `dbo.NYC_Payroll_Data_2020`
5. Import schema: From connection/store
6. OK

### ds_NYC_Payroll_Data_2021
1. + > Azure SQL Database > Continue
2. Name: `ds_NYC_Payroll_Data_2021`
3. Linked service: `ls_SqlDatabase`
4. Table: `dbo.NYC_Payroll_Data_2021`
5. Import schema: From connection/store
6. OK

### ds_NYC_Payroll_Summary
1. + > Azure SQL Database > Continue
2. Name: `ds_NYC_Payroll_Summary`
3. Linked service: `ls_SqlDatabase`
4. Table: `dbo.NYC_Payroll_Summary`
5. Import schema: From connection/store
6. OK

**Click "Publish all" button at top**

---

## PART 3: Synapse Dataset (1)

### ds_Synapse_NYC_Payroll_Summary
1. + next to Datasets > **Azure Synapse Analytics** > Continue
2. Name: `ds_Synapse_NYC_Payroll_Summary`
3. Linked service: `ls_Synapse`
4. Table name: Type `dbo.NYC_Payroll_Summary` (or select from dropdown)
5. Import schema: **None** (skip - file doesn't exist yet)
6. OK
7. Leave schema empty - pipeline will handle it

**Click "Publish all" button at top**

---

## Verification

You should see 12 datasets in Author view:
- 5 CSV datasets (file icon)
- 6 SQL datasets (table icon)
- 1 Synapse dataset (table icon)

Take screenshot showing all 12 datasets listed

### CSV Source Datasets (5)
1. `ds_AgencyMaster` - Agency reference data
2. `ds_EmpMaster` - Employee reference data
3. `ds_TitleMaster` - Job title reference data
4. `ds_nycpayroll_2020` - Historical payroll data
5. `ds_nycpayroll_2021` - Current payroll data

### SQL Table Datasets (6)
6. `ds_NYC_Payroll_AGENCY_MD` - Agency dimension table
7. `ds_NYC_Payroll_EMP_MD` - Employee dimension table
8. `ds_NYC_Payroll_TITLE_MD` - Title dimension table
9. `ds_NYC_Payroll_Data_2020` - 2020 fact table
10. `ds_NYC_Payroll_Data_2021` - 2021 fact table
11. `ds_NYC_Payroll_Summary` - Aggregated summary table

### Synapse Dataset (1)
12. `ds_Synapse_NYC_Payroll_Summary` - External table in Synapse

---

## Part 1: CSV Source Datasets

### 1. ds_AgencyMaster

1. In Data Factory Studio, click **Author** (pencil icon)
2. Click **+** next to Datasets
3. Select **Azure Data Lake Storage Gen2**
4. Select format: **DelimitedText**
5. Click **Continue**

**Configuration:**
```
Name: ds_AgencyMaster
Linked service: ls_AdlsGen2
File path:
  - Container: dirpayrollfiles
  - Directory: (leave blank)
  - File: AgencyMaster.csv
First row as header: ✓ (checked)
Import schema: From connection/store
```

6. Click **OK**
7. Click **Publish all** (top of page)

---

### 2. ds_EmpMaster

Repeat steps above with:
```
Name: ds_EmpMaster
Linked service: ls_AdlsGen2
File path:
  - Container: dirpayrollfiles
  - Directory: (leave blank)
  - File: EmpMaster.csv
First row as header: ✓
Import schema: From connection/store
```

---

### 3. ds_TitleMaster

Repeat steps above with:
```
Name: ds_TitleMaster
Linked service: ls_AdlsGen2
File path:
  - Container: dirpayrollfiles
  - Directory: (leave blank)
  - File: TitleMaster.csv
First row as header: ✓
Import schema: From connection/store
```

---

### 4. ds_nycpayroll_2020

Repeat steps above with:
```
Name: ds_nycpayroll_2020
Linked service: ls_AdlsGen2
File path:
  - Container: dirhistoryfiles
  - Directory: (leave blank)
  - File: nycpayroll_2020.csv
First row as header: ✓
Import schema: From connection/store
```

---

### 5. ds_nycpayroll_2021

Repeat steps above with:
```
Name: ds_nycpayroll_2021
Linked service: ls_AdlsGen2
File path:
  - Container: dirpayrollfiles
  - Directory: (leave blank)
  - File: nycpayroll_2021.csv
First row as header: ✓
Import schema: From connection/store
```

**After creating all 5 CSV datasets, click "Publish all"**

---

## Part 2: SQL Table Datasets

### 6. ds_NYC_Payroll_AGENCY_MD

1. Click **+** next to Datasets
2. Select **Azure SQL Database**
3. Click **Continue**

**Configuration:**
```
Name: ds_NYC_Payroll_AGENCY_MD
Linked service: ls_SqlDatabase
Table name: dbo.NYC_Payroll_AGENCY_MD
Import schema: From connection/store
```

4. Click **OK**

---

### 7. ds_NYC_Payroll_EMP_MD

Repeat steps above with:
```
Name: ds_NYC_Payroll_EMP_MD
Linked service: ls_SqlDatabase
Table name: dbo.NYC_Payroll_EMP_MD
Import schema: From connection/store
```

---

### 8. ds_NYC_Payroll_TITLE_MD

Repeat steps above with:
```
Name: ds_NYC_Payroll_TITLE_MD
Linked service: ls_SqlDatabase
Table name: dbo.NYC_Payroll_TITLE_MD
Import schema: From connection/store
```

---

### 9. ds_NYC_Payroll_Data_2020

Repeat steps above with:
```
Name: ds_NYC_Payroll_Data_2020
Linked service: ls_SqlDatabase
Table name: dbo.NYC_Payroll_Data_2020
Import schema: From connection/store
```

---

### 10. ds_NYC_Payroll_Data_2021

Repeat steps above with:
```
Name: ds_NYC_Payroll_Data_2021
Linked service: ls_SqlDatabase
Table name: dbo.NYC_Payroll_Data_2021
Import schema: From connection/store
```

---

### 11. ds_NYC_Payroll_Summary

Repeat steps above with:
```
Name: ds_NYC_Payroll_Summary
Linked service: ls_SqlDatabase
Table name: dbo.NYC_Payroll_Summary
Import schema: From connection/store
```

**After creating all 6 SQL datasets, click "Publish all"**

---

## Part 3: Synapse Dataset

### 12. ds_Synapse_NYC_Payroll_Summary

1. Click **+** next to Datasets
2. Select **Azure Synapse Analytics**
3. Click **Continue**

**Configuration:**
```
Name: ds_Synapse_NYC_Payroll_Summary
Linked service: ls_Synapse
Table name: dbo.NYC_Payroll_Summary
Import schema: None (skip - data doesn't exist yet)
```

4. Click **OK** (schema will be empty - this is expected)
5. Click **Publish all**

---

## Verification

You should now see **12 datasets** in the Author view:

**CSV Datasets (5):**
- ds_AgencyMaster
- ds_EmpMaster
- ds_TitleMaster
- ds_nycpayroll_2020
- ds_nycpayroll_2021

**SQL Datasets (6):**
- ds_NYC_Payroll_AGENCY_MD
- ds_NYC_Payroll_EMP_MD
- ds_NYC_Payroll_TITLE_MD
- ds_NYC_Payroll_Data_2020
- ds_NYC_Payroll_Data_2021
- ds_NYC_Payroll_Summary

**Synapse Dataset (1):**
- ds_Synapse_NYC_Payroll_Summary

---

## Screenshot Checklist

Take screenshot showing:
- All 12 datasets listed in Author view
- Dataset names visible
- Icons showing different types (file vs table)

---

## Data Engineering Concept

### Why Separate Datasets?

**Reusability:** Same dataset can be used in multiple pipelines

**Parameterization:** Can make datasets dynamic (e.g., `nycpayroll_${year}.csv`)

**Schema Evolution:** Update schema in one place, affects all pipelines using it

**Testing:** Can preview data from dataset without running full pipeline

### Dataset Types

**DelimitedText (CSV):** 
- Flexible, human-readable
- Good for data exchange
- Slower to query (must parse text)

**SQL Table:** 
- Structured, enforces types
- Fast queries with indexes
- ACID transactions

**External Table (Synapse):**
- Best of both worlds
- Query files like tables
- No data movement

---

## Next Steps

After creating all 12 datasets:
1. Take screenshot
2. Proceed to Step 4: Create Data Flows
