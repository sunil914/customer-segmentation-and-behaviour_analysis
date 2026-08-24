# Customer Segmentation & Behaviour Analysis

> **Status:** Core RFM analysis documented · Tableau dashboard in progress

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

## Tableau dashboard — in progress

Planned views:

- Revenue and customer count by RFM segment
- Recency vs Monetary scatter, sized by Frequency
- Segment profile heatmap
- Country revenue comparison
- Monthly revenue and top-product analysis
- Interactive RFM and geography filters

## Key insights

- Clean revenue totalled **£8.91M** from **18,532 orders** and **4,338 customers**.
- Champions were the highest-revenue segment and contained 478 customers.
- A total of 656 customers were classified as At Risk.
- Customer value was strongly concentrated, so average order value alone does not describe the distribution.

## Repository roadmap

- [x] Business problem and KPI definition
- [x] Cleaning and RFM methodology
- [x] SQL analysis documented
- [x] Findings and retention recommendations documented
- [x] Add cleaned data with source and validation notes
- [ ] Add reproducible preparation code
- [ ] Add complete SQL script and analysis outputs
- [ ] Build and publish Tableau dashboard
- [ ] Add dashboard screenshots and Tableau Public link

## Responsible interpretation

Anonymous identifiers are used only for aggregate behavioural analysis. RFM describes transaction history; it does not infer personal characteristics or guarantee future purchasing.
