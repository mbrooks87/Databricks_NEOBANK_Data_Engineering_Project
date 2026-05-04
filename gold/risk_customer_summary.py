CREATE OR REPLACE TABLE banking.gold.risk_customer_summary AS

SELECT
risk_grade,
COUNT(customer_id) AS total_customers,
AVG(credit_score) AS avg_credit_score,
SUM(external_active_loans) AS total_external_loans,
SUM(external_overdue_amount) AS total_overdue_amount

FROM banking.silver.credit_bureau_reports

GROUP BY risk_grade

count = spark.sql("""
SELECT COUNT(*) AS cnt
FROM banking.gold.risk_customer_summary
""").collect()[0]["cnt"]

dbutils.notebook.exit(str(count))
