# 🥈 Silver Layer — Cleansed & Conformed

The Silver layer applies **deduplication, watermark filtering, and merge logic** to produce clean, reliable tables ready for analytics and Gold transformations.

## Notebook

| File | Description |
|------|-------------|
| `04_Bronze_to_Silver.py` | Reads from Bronze, applies load strategy (FULL / APPEND / MERGE), writes to `banking.silver.*` |

## How It Works

1. Reads `table_metadata` and `table_parameters` from widgets
2. Reads the Bronze Delta table and filters by watermark (for APPEND/MERGE)
3. Adds `insert_timestamp` and `update_timestamp` audit columns
4. Writes to Silver using the configured load strategy:
   - **FULL** — overwrites the Silver table entirely
   - **APPEND** — appends new records only
   - **MERGE** — upserts using the primary key (Delta `MERGE INTO`)
5. Updates `banking.metadata.table_watermarks` with the latest processed value
6. Updates `banking.metadata.pipeline_runs` with final run status and record count

## Silver Tables Produced

| Table | Load Type | Primary Key |
|-------|-----------|-------------|
| banking.silver.customers | MERGE | customer_id |
| banking.silver.accounts | MERGE | account_id |
| banking.silver.transactions | APPEND | txn_id |
| banking.silver.branches | FULL | branch_code |
| banking.silver.credit_bureau_reports | MERGE | customer_id |
| banking.silver.payment_gateway_logs | APPEND | txn_id |

## Output

Clean Delta tables in `banking.silver.*` with full audit columns and accurate watermark tracking.
