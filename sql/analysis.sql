DROP VIEW IF EXISTS v_project_kpis;
DROP VIEW IF EXISTS v_order_summary;
DROP VIEW IF EXISTS v_customer_rfm;
DROP VIEW IF EXISTS v_customer_rfm_scores;
DROP VIEW IF EXISTS v_customer_segments;
DROP VIEW IF EXISTS v_monthly_revenue;
DROP VIEW IF EXISTS v_country_performance;
DROP VIEW IF EXISTS v_product_performance;

CREATE VIEW v_project_kpis AS
SELECT
    COUNT(*) AS line_items,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(DISTINCT invoice_no) AS orders,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(revenue) / COUNT(DISTINCT invoice_no), 2) AS average_order_value
FROM customer_sales;

CREATE VIEW v_order_summary AS
SELECT
    invoice_no,
    customer_id,
    MIN(invoice_date) AS order_date,
    SUM(quantity) AS units,
    ROUND(SUM(revenue), 2) AS order_revenue
FROM customer_sales
GROUP BY invoice_no, customer_id;

CREATE VIEW v_customer_rfm AS
WITH anchor AS (
    SELECT datetime(MAX(invoice_date), '+1 day') AS analysis_date
    FROM customer_sales
)
SELECT
    s.customer_id,
    CAST(julianday(anchor.analysis_date) - julianday(MAX(s.invoice_date)) AS INTEGER) AS recency_days,
    COUNT(DISTINCT s.invoice_no) AS frequency,
    ROUND(SUM(s.revenue), 2) AS monetary
FROM customer_sales AS s
CROSS JOIN anchor
GROUP BY s.customer_id;

CREATE VIEW v_customer_rfm_scores AS
SELECT
    customer_id,
    recency_days,
    frequency,
    monetary,
    6 - NTILE(5) OVER (ORDER BY recency_days ASC, customer_id) AS r_score,
    NTILE(5) OVER (ORDER BY frequency ASC, customer_id) AS f_score,
    NTILE(5) OVER (ORDER BY monetary ASC, customer_id) AS m_score
FROM v_customer_rfm;

CREATE VIEW v_customer_segments AS
SELECT
    *,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal'
        WHEN r_score >= 4 AND f_score BETWEEN 2 AND 3 THEN 'Potential Loyalists'
        WHEN r_score = 5 AND f_score = 1 THEN 'New'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score = 3 AND f_score <= 2 THEN 'Needs Attention'
        ELSE 'Hibernating'
    END AS segment
FROM v_customer_rfm_scores;

CREATE VIEW v_monthly_revenue AS
SELECT
    substr(invoice_date, 1, 7) AS month,
    COUNT(DISTINCT invoice_no) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(revenue), 2) AS revenue
FROM customer_sales
GROUP BY substr(invoice_date, 1, 7);

CREATE VIEW v_country_performance AS
SELECT
    country,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(DISTINCT invoice_no) AS orders,
    ROUND(SUM(revenue), 2) AS revenue
FROM customer_sales
GROUP BY country;

CREATE VIEW v_product_performance AS
SELECT
    stock_code,
    description,
    SUM(quantity) AS units,
    ROUND(SUM(revenue), 2) AS revenue
FROM customer_sales
GROUP BY stock_code, description;
