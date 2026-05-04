# ⚙️ Metadata Layer — Pipeline Configuration & Orchestration

The Metadata layer is the **control plane** of the entire pipeline. It stores configuration, tracks watermarks, and logs every pipeline run for full observability.

## Notebooks

| File | Description |
|------|-------------|
| `00_Setup_Secret_Scope.py` | Creates the Databricks Secret Scope and stores the SQL Server connection JSON and Gmail API key |
| `01_Setup_Metadata.sql` | Creates all metadata tables, the source volume, and inserts initial config for all 11 tables |
| `02_Check_Metadata.sql` | Quick inspection queries for all metadata tables |
| `01_Read_Tables_List.py` | Reads active tables from `metadata.tables` for a given source system and passes them as a task value |
| `02_Read_Table_Parameters.py` | Reads load config (load_type, primary_key, watermark_column) for a specific table and passes as task value |

## Metadata Tables

### `banking.metadata.tables`
Central registry of all source and Gold tables. Controls which tables are active and in what order they load.

| Column | Description |
|--------|-------------|
| table_id | Unique identifier |
| table_name | Logical table name |
| source_system | `sqlserver`, `blob`, or `silver` |
| source_path | Blob volume path (for CSV sources) |
| target_layer | `silver` or `gold` |
| active_flag | Enables/disables table from pipeline |
| load_order | Processing sequence |

### `banking.metadata.table_parameters`
Key-value store for per-table processing config.

| parameter_name | Values |
|----------------|--------|
| load_type | `FULL`, `APPEND`, `MERGE` |
| primary_key | Column used for MERGE deduplication |
| watermark_column | Column used for incremental filtering |

### `banking.metadata.table_watermarks`
Tracks the last successfully processed watermark per table. Reset to `1900-01-01` on initial load.

### `banking.metadata.pipeline_runs`
Full audit log of every pipeline execution with start/end time, status, record count, and error messages.

## Registered Tables

| table_id | table_name | Source | Layer |
|----------|-----------|--------|-------|
| 1 | customers | SQL Server | Silver |
| 2 | accounts | SQL Server | Silver |
| 3 | transactions | SQL Server | Silver |
| 4 | branches | SQL Server | Silver |
| 5 | credit_bureau_reports | Blob CSV | Silver |
| 6 | payment_gateway_logs | Blob CSV | Silver |
| 7 | customer_360 | Silver | Gold |
| 8 | branch_performance | Silver | Gold |
| 9 | transaction_channel_summary | Silver | Gold |
| 10 | daily_bank_kpi | Silver | Gold |
| 11 | risk_customer_summary | Silver | Gold |
