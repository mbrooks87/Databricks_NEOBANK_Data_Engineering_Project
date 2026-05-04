CREATE OR REPLACE TABLE banking.gold.transaction_channel_summary AS

SELECT
DATE(t.txn_timestamp) AS txn_date,
pg.gateway_name,
pg.device_type,

COUNT(*) AS total_transactions,

SUM(
    CASE WHEN pg.gateway_status = 'SUCCESS'
    THEN 1 ELSE 0 END
) AS successful_transactions,

SUM(
    CASE WHEN pg.gateway_status = 'FAILED'
    THEN 1 ELSE 0 END
) AS failed_transactions,

AVG(pg.processing_time_ms) AS avg_processing_time_ms

FROM banking.silver.transactions t

JOIN banking.silver.payment_gateway_logs pg
    ON t.txn_id = pg.txn_id

GROUP BY
txn_date,
pg.gateway_name,
pg.device_type

count = spark.sql("""
SELECT COUNT(*) AS cnt
FROM banking.gold.transaction_channel_summary
""").collect()[0]["cnt"]

dbutils.notebook.exit(str(count))
