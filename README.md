# Customer Segmentation & Behaviour Analysis

> **Status:** Validated data and executable SQLite analysis complete · Tableau dashboard in progress

## Overview

This project transforms the UCI Online Retail transaction dataset into a customer-level RFM model to identify high-value customers, loyalty opportunities and retention risk.

**Dataset:** [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online%2Bretail) · CC BY 4.0

## Key KPIs

| Metric | Result |
|---|---:|
| Clean revenue | £8.91M |
| Customers | 4,338 |
| Completed orders | 18,532 |
| Average order value | £480.87 |
| Valid sales rows | 397,884 |

## Analysis completed

- Removed cancellations, non-positive quantities/prices and transactions without customer IDs.
- Created line revenue and chronological fields.
- Calculated customer Recency, Frequency and Monetary values.
- Assigned quintile R, F and M scores.
- Created Champions, Loyal, Potential Loyalists, New, At Risk, Needs Attention and Hibernating segments.
- Reconciled customer revenue to order, product, country and monthly totals.

## Repository contents

- [`data/`](data/) — cleaned full dataset, preview sample, source and validation notes
- [`sql/`](sql/) — executable SQLite schema, RFM analysis views and run guide
- [`scripts/build_database.py`](scripts/build_database.py) — standard-library loader that rebuilds and validates `project.db`
- Tableau build guide below — workbook, Tableau Public link and screenshots are still pending

## Tableau dashboard build guide — in progress

The dashboard has not been built or published yet. The following specification turns the validated SQLite views into a reproducible Tableau Public workflow.

### 1. Prepare Tableau-ready files

1. Run `python3 scripts/build_database.py` from the repository root.
2. Open the generated `project.db` in DB Browser for SQLite.
3. Export each of these views as a CSV with headers:
   - `v_project_kpis`
   - `v_customer_segments`
   - `v_monthly_revenue`
   - `v_country_performance`
   - `v_product_performance`
4. Connect the exported CSVs in Tableau. Keep `customer_id` as a string and revenue fields as decimal numbers.

Before designing charts, reconcile **397,884 sales lines**, **4,338 customers**, **18,532 orders**, **£8,911,407.90 revenue**, **£480.87 average order value**, **947 Champions** and **661 At Risk customers**.

### 2. Build the worksheets

| Worksheet | Source | Tableau specification |
|---|---|---|
| KPI strip | `v_project_kpis` | Text marks for Revenue, Customers, Orders and Average Order Value |
| Segment overview | `v_customer_segments` | Segment on Rows; `COUNTD(customer_id)` and `SUM(monetary)`; sort by revenue |
| RFM scatter | `v_customer_segments` | Recency on Columns, Monetary on Rows, Customer ID on Detail, Frequency on Size and Segment on Colour |
| Segment profile | `v_customer_segments` | Segment on Rows; average Recency, Frequency and Monetary as Measure Values |
| Country performance | `v_country_performance` | Country on Rows and Revenue on Columns; show Customers and Orders in tooltips |
| Monthly trend | `v_monthly_revenue` | Month on Columns and Revenue on Rows; use a continuous chronological month |
| Product performance | `v_product_performance` | Description on Rows and Revenue on Columns; apply a Top 10 revenue filter |

Use consistent currency formatting and show definitions in tooltips. For the scatter plot, lower recency represents a more recent purchase.

### 3. Assemble and test the dashboard

- Place the KPI strip first, followed by Segment overview and RFM scatter, then the supporting country, monthly and product views.
- Add Segment and Country filters; apply each only to worksheets with compatible fields.
- Add a Segment overview filter action so selecting a segment highlights the relevant customers.
- Use a colour-blind-safe palette, retain text labels for important values and avoid encoding meaning with colour alone.
- Provide descriptive worksheet titles, readable tooltips, logical tab order and sufficient contrast.
- Recheck every KPI after filters are cleared and test the layout at desktop and phone sizes.

### 4. Publish checklist

- [ ] Build the Tableau workbook from the exported SQLite views
- [ ] Reconcile unfiltered totals with `v_project_kpis`
- [ ] Test filters, actions, tooltips and accessibility
- [ ] Publish to Tableau Public
- [ ] Add desktop and mobile screenshots
- [ ] Add the workbook, screenshots and live dashboard link to this repository

## Key insights

- Clean revenue totalled **£8.91M** from **18,532 orders** and **4,338 customers**.
- The executable scoring rules classify 947 customers as Champions and 661 as At Risk.
- Customer value was strongly concentrated, so average order value alone does not describe the distribution.

## Repository roadmap

- [x] Business problem and KPI definition
- [x] Cleaning and RFM methodology
- [x] SQL analysis documented
- [x] Findings and retention recommendations documented
- [x] Add cleaned data with source and validation notes
- [x] Add reproducible SQLite database loader
- [ ] Add reproducible preparation code
- [x] Add complete SQL schema and analysis views
- [ ] Build and publish Tableau dashboard
- [ ] Add dashboard screenshots and Tableau Public link

## Responsible interpretation

Anonymous identifiers are used only for aggregate behavioural analysis. RFM describes transaction history; it does not infer personal characteristics or guarantee future purchasing.
