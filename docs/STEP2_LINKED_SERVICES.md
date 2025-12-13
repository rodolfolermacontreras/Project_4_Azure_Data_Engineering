# Step 2: Create Linked Services in Azure Data Factory

## Overview
Linked Services define connections to external resources. Think of them as connection strings with credentials.

---

## 1. ADLS Gen2 Linked Service

### Purpose
Allows Data Factory to read CSV files from Data Lake

### Steps
1. Open Data Factory Studio: https://adf.azure.com
2. Select workspace: `adf-nycpayroll-rodolfo-l`
3. Click **Manage** (toolbox icon on left)
4. Click **Linked services**
5. Click **+ New**
6. Search for: **Azure Data Lake Storage Gen2**
7. Click **Continue**

### Configuration
```
Name: ls_AdlsGen2
Description: Connection to Data Lake for CSV files

Authentication method: Account key
Account selection method: From Azure subscription
Azure subscription: UdacityDS - 195
Storage account name: adlsnycpayrollrodolfol

Test connection: To linked service
```

8. Click **Test connection** (should succeed)
9. Click **Create**

---

## 2. Azure SQL Database Linked Service

### Purpose
Allows Data Factory to write data to SQL tables

### Steps
1. Still in **Linked services** page
2. Click **+ New**
3. Search for: **Azure SQL Database**
4. Click **Continue**

### Configuration
```
Name: ls_SqlDatabase
Description: Connection to SQL Database

Connect via integration runtime: AutoResolveIntegrationRuntime
Account selection method: From Azure subscription
Azure subscription: UdacityDS - 195
Server name: sqlserver-nycpayroll-rodolfo-l
Database name: db_nycpayroll

Authentication type: SQL authentication
User name: sqladmin
Password: P@ssw0rd1234!

Test connection: To linked service
```

5. Click **Test connection** (should succeed)
6. Click **Create**

---

## 3. Synapse Linked Service

### Purpose
Allows Data Factory to execute CETAS in Synapse

### Steps
1. Still in **Linked services** page
2. Click **+ New**
3. Search for: **Azure Synapse Analytics**
4. Click **Continue**

### Configuration
```
Name: ls_Synapse
Description: Connection to Synapse serverless SQL

Connect via integration runtime: AutoResolveIntegrationRuntime
Account selection method: Enter manually
Server name: synapse-nycpayroll-rodolfo-l-ondemand.sql.azuresynapse.net
Database name: udacity

Authentication type: SQL authentication
User name: sqladmin
Password: P@ssw0rd1234!

Test connection: To linked service
```

5. Click **Test connection** (should succeed)
6. Click **Create**

---

## Verification

You should now see 3 linked services:
- ls_AdlsGen2 (Type: AzureBlobFS)
- ls_SqlDatabase (Type: AzureSqlDatabase)  
- ls_Synapse (Type: AzureSqlDW)

---

## Screenshot Checklist

Take screenshot showing:
- All 3 linked services listed
- Name and Type columns visible
- Green checkmarks indicating successful connection tests

---

## Data Engineering Concept

### Linked Services vs Datasets

**Linked Service** = WHERE the data is
- Connection configuration
- Credentials
- Server/account name

**Dataset** = WHAT the data looks like
- Schema definition
- Column names and types
- File format

### Analogy
- Linked Service = Database connection string (`host`, `username`, `password`)
- Dataset = Table name + column definitions (`SELECT * FROM table`)

---

## Next Steps

Step 2 complete. Proceed to STEP3_DATASETS.md
