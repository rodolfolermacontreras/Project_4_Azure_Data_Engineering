"""
Step 2: Upload CSV Files to Azure Data Lake Storage Gen2

WHY THIS MATTERS:
In data engineering, raw data must be uploaded to cloud storage (Data Lake)
before it can be processed by data pipelines. This is the "ingest" phase.

We separate historical (2020) and current (2021) data for:
- Data lineage tracking
- Access control
- Preventing accidental overwrites
- Following Bronze/Silver/Gold architecture patterns
"""

import subprocess
import os

# Configuration
STORAGE_ACCOUNT = "adlsnycpayrollrodolfol"
# Get absolute path to data folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
DATA_PATH = os.path.join(PROJECT_ROOT, "data")

# Files to upload and their destinations
FILE_MAPPINGS = {
    # Master data files - go to both directories for reference
    "AgencyMaster.csv": ["dirpayrollfiles", "dirhistoryfiles"],
    "EmpMaster.csv": ["dirpayrollfiles", "dirhistoryfiles"],
    "TitleMaster.csv": ["dirpayrollfiles", "dirhistoryfiles"],
    
    # Historical payroll data
    "nycpayroll_2020.csv": ["dirhistoryfiles"],
    
    # Current payroll data
    "nycpayroll_2021.csv": ["dirpayrollfiles"]
}

def run_command(command, description):
    """Execute command and handle errors"""
    print(f"\n{'='*70}")
    print(f"STEP: {description}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print("SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.stderr}")
        return False

def upload_file(local_file, container, storage_account):
    """
    Upload a file to Azure Data Lake Storage Gen2
    
    WHY WE USE AZURE CLI:
    - Simple authentication (already logged in)
    - Reliable file transfer
    - Automatic retry on network issues
    
    For large-scale production, we'd use:
    - Azure Data Factory for scheduled ingestion
    - Azure Storage SDKs for programmatic control
    - AzCopy for bulk transfers
    """
    file_path = os.path.join(DATA_PATH, local_file)
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return False
    
    command = f"""az storage blob upload \
        --account-name {storage_account} \
        --container-name {container} \
        --name {local_file} \
        --file "{file_path}" \
        --auth-mode login \
        --overwrite"""
    
    return run_command(
        command,
        f"Upload {local_file} to {container}"
    )

def verify_uploads(storage_account):
    """
    List all files in each container to verify uploads
    
    WHY VERIFICATION MATTERS:
    - Ensures data integrity
    - Confirms file availability for pipelines
    - Catches upload failures early
    """
    print(f"\n{'='*70}")
    print("VERIFYING UPLOADS")
    print(f"{'='*70}")
    
    for container in ["dirpayrollfiles", "dirhistoryfiles", "dirstaging"]:
        print(f"\nContainer: {container}")
        print("-" * 70)
        
        command = f"""az storage blob list \
            --account-name {storage_account} \
            --container-name {container} \
            --auth-mode login \
            --query "[].name" \
            --output tsv"""
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            if files and files[0]:
                for f in files:
                    print(f"  - {f}")
            else:
                print("  (empty)")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {e.stderr}")

def print_summary():
    """Print summary with data engineering concepts"""
    print(f"\n{'='*70}")
    print("DATA UPLOAD COMPLETE")
    print(f"{'='*70}")
    
    print("""
DATA ENGINEERING CONCEPTS APPLIED:

1. SEPARATION OF CONCERNS:
   - Historical data (2020) in dirhistoryfiles
   - Current data (2021) in dirpayrollfiles
   - Master data duplicated for independence
   
2. DATA LINEAGE:
   - Clear folder structure shows data origins
   - Historical vs current data easily identified
   - Staging area ready for transformations

3. BRONZE/SILVER/GOLD ARCHITECTURE:
   - Bronze Layer = Raw data as ingested (our current state)
   - Silver Layer = Cleaned, validated data (after ADF pipelines)
   - Gold Layer = Aggregated, business-ready data (NYC_Payroll_Summary)

4. NEXT STEPS IN PIPELINE:
   - Data Factory will read from dirpayrollfiles and dirhistoryfiles
   - Apply transformations (clean, join, aggregate)
   - Write to SQL Database (silver layer)
   - Write aggregated summary to Synapse (gold layer)

WHY THIS MATTERS FOR DATA SCIENTISTS:
- Raw data preservation ensures reproducibility
- Clear folder structure aids collaboration
- Separation enables parallel processing
- Follows industry best practices for production systems
""")

def main():
    """Upload all CSV files to appropriate containers"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║              UPLOAD DATA TO AZURE DATA LAKE GEN2                  ║
    ║                     Data Ingestion Phase                          ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    print("\nThis script will upload 5 CSV files to the Data Lake.")
    print("Estimated time: 2-3 minutes")
    
    input("\nPress Enter to start...")
    
    # Upload each file to its designated container(s)
    upload_count = 0
    total_count = sum(len(containers) for containers in FILE_MAPPINGS.values())
    
    for filename, containers in FILE_MAPPINGS.items():
        for container in containers:
            if upload_file(filename, container, STORAGE_ACCOUNT):
                upload_count += 1
    
    print(f"\n{'='*70}")
    print(f"Upload Results: {upload_count}/{total_count} files uploaded")
    print(f"{'='*70}")
    
    # Verify uploads
    verify_uploads(STORAGE_ACCOUNT)
    
    # Print summary
    print_summary()
    
    print("\nNEXT STEP: Create SQL tables using script 03_create_sql_tables.py")

if __name__ == "__main__":
    main()
