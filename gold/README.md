# 🥇 Gold Layer — Business-Ready Analytics Tables

The Gold layer contains **aggregated, business-logic-enriched** tables built from Silver. These tables directly power the NEOBank Dashboard, Genie Spaces, and BI reporting.

## Notebooks

| File | Description |
|------|-------------|
| `01_Silver_to_Gold_Driver.py` | Orchestration driver — logs audit entry, dynamically calls the correct Gold notebook by table name |
| `customer_360.py` | Full customer profile: accounts, balances, transactions, credit score, risk grade, and segment |
| `branch_performance.py` | Branch-level aggregation: total customers, deposits, and transaction volume |
| `transaction_channel_summary.py` | Daily transaction breakdown by payment gateway and device type |
| `daily_bank_kpi.py` | Daily snapshot KPIs: total customers, accounts, balances, transactions, avg credit score, high-risk count |
| `risk_customer_summary.py` | Risk grade summary: customer count, avg credit score, total loans, and overdue amounts |

## How It Works

The `01_Silver_to_Gold_Driver.py` notebook:
1. Receives `run_id` and `table_metadata` as widgets from the job orchestrator
2. Creates/updates an audit entry in `banking.metadata.pipeline_runs`
3. Dynamically calls `gold_transformations/<table_name>` notebook via `dbutils.notebook.run()`
4. Captures the record count returned by the Gold notebook and updates the audit log

Each Gold notebook:
- Runs a `CREATE OR REPLACE TABLE` using Silver joins/aggregations
- Returns the final record count via `dbutils.notebook.exit(str(count))`

## Gold Tables Produced

| Table | Source Tables | Description |
|-------|--------------|-------------|
| `banking.gold.customer_360` | customers, accounts, transactions, branches, credit_bureau_reports | Full 360 view per customer |
| `banking.gold.branch_performance` | branches, customers, accounts, transactions | KPIs aggregated per branch |
| `banking.gold.transaction_channel_summary` | transactions, payment_gateway_logs | Daily success/fail rates by gateway & device |
| `banking.gold.daily_bank_kpi` | transactions, customers, accounts, credit_bureau_reports | Daily bank-wide KPI snapshot |
| `banking.gold.risk_customer_summary` | credit_bureau_reports | Risk tier breakdown with loan exposure |

## Customer Segmentation Logic

Applied in `customer_360.py`:

| Segment | Criteria |
|---------|----------|
| HIGH_VALUE | Total balance ≥ $500,000 |
| MEDIUM_VALUE | Total balance ≥ $100,000 |
| LOW_VALUE | Total balance < $100,000 |
