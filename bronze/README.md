# 🥉 Bronze Layer — Raw Ingestion

The Bronze layer is the **landing zone** for all raw data ingested from source systems. No transformations are applied — data lands exactly as it arrives, with an `insert_timestamp` appended for lineage.

## Notebook

| File | Description |
|------|-------------|
| `03_Source_to_Bronze.py` | Ingests data from SQL Server (JDBC) and Azure Blob Storage (Auto Loader) into Delta Bronze tables |

## How It Works

1. Reads `table_metadata` and `table_parameters` widgets passed from the orchestration layer
2. Retrieves the SQL Server connection string from **Databricks Secret Scope** (`banking-scope`)
3. For incremental tables (MERGE/APPEND), fetches the last watermark from `banking.metadata.table_watermarks` to only pull new/changed records
4. Reads source data via:
   - **JDBC** for SQL Server tables (`customers`, `accounts`, `transactions`, `branches`)
   - **Auto Loader (cloudFiles)** for CSV files on Blob Storage (`credit_bureau_reports`, `payment_gateway_logs`)
5. Appends raw data to `banking.bronze.<table_name>` Delta tables
6. Updates `banking.metadata.pipeline_runs` with run status (INPROGRESS / SUCCESS / FAILED)

## Source Tables Ingested

| Table | Source System | Load Type | Watermark Column |
|-------|--------------|-----------|-----------------|
| customers | SQL Server | MERGE | updated_at |
| accounts | SQL Server | MERGE | updated_at |
| transactions | SQL Server | APPEND | txn_timestamp |
| branches | SQL Server | FULL | — |
| credit_bureau_reports | Blob CSV | MERGE | bureau_pull_date |
| payment_gateway_logs | Blob CSV | APPEND | processed_timestamp |

## Output

All raw records are written to `banking.bronze.*` as append-only Delta tables with an added `insert_timestamp` column.
