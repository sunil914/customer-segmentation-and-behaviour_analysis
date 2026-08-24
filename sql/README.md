# SQLite analysis

Build the database from the committed cleaned data using only Python's standard library:

```bash
python3 scripts/build_database.py
```

The command reconstructs the multipart gzip file, loads 397,884 line items into `project.db`, checks the row count and database integrity, then creates reusable views.

## Analysis views

- `v_project_kpis` — customers, orders, revenue and average order value
- `v_order_summary` — one row per customer order
- `v_customer_rfm` and `v_customer_rfm_scores` — reproducible Recency, Frequency and Monetary measures
- `v_customer_segments` — documented rule-based customer groups
- `v_monthly_revenue`, `v_country_performance`, `v_product_performance` — Tableau-ready aggregates

Expected reconciliation: **4,338 customers**, **18,532 orders**, **£8,911,407.90 revenue** and **£480.87 average order value**. The generated `project.db` can be opened in DB Browser for SQLite; it is intentionally ignored by Git because it can be rebuilt.

