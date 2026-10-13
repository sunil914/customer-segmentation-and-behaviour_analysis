# Tableau Dashboard Build Guide

> **Status:** Build specification only. The Tableau workbook, screenshots and Tableau Public link are not yet published.

## Purpose

Build a customer-segmentation dashboard from the repository's validated SQLite exports. The dashboard should explain customer value, recency, purchase frequency, segment size, country performance, monthly revenue and product performance without joining incompatible aggregates or implying that RFM labels are permanent personal traits.

## 1. Generate the verified sources

From the repository root, run:

```bash
python3 scripts/build_database.py
python3 scripts/export_tableau_data.py
```

The exporter checks SQLite integrity and reconciles 397,884 valid sales lines, 4,338 customers, 18,532 completed orders, £8,911,407.90 revenue, £480.87 average order value, 947 Champions and 661 At Risk customers before atomically replacing the export set.

Connect Tableau only to these files:

| Export | Grain | Fields | Intended use |
|---|---|---|---|
| `project_kpis.csv` | One project row | `line_items`, `customers`, `orders`, `revenue`, `average_order_value` | Opening KPI strip |
| `customer_segments.csv` | One row per customer | `customer_id`, `recency_days`, `frequency`, `monetary`, `r_score`, `f_score`, `m_score`, `segment` | Segment, scatter and profile views |
| `monthly_revenue.csv` | One row per month | `month`, `orders`, `customers`, `revenue` | Monthly trend |
| `country_performance.csv` | One row per country | `country`, `customers`, `orders`, `revenue` | Country ranking |
| `product_performance.csv` | One row per stock-code/description pair | `stock_code`, `description`, `units`, `revenue` | Product ranking |

Keep `customer_id` as text, parse `month` as a chronological date and format revenue and monetary measures as GBP.

## 2. Data-model boundary

Use the exports as separate logical tables or separate data sources. Do not physically join them and do not create many-to-many relationships merely to enable global filters.

The files intentionally have different grains:

- `project_kpis.csv` is a fixed, validated project total.
- `customer_segments.csv` contains customer-level RFM measures but no country, month, order or product key.
- The month, country and product files are independent aggregates without customer-level segment fields.

A join on no key, a calculated constant or a non-unique field can multiply rows and inflate revenue, customers or orders. Validate each worksheet against its own export and use dashboard actions only where the target source has compatible fields.

## 3. Core calculations

Create these fields only in the `customer_segments.csv` data source.

### Customers

```text
COUNTD([customer_id])
```

### Segment revenue

```text
SUM([monetary])
```

### Revenue per customer

```text
IF COUNTD([customer_id]) = 0 THEN 0
ELSE SUM([monetary]) / COUNTD([customer_id])
END
```

### Recency direction label

```text
"Lower recency means a more recent purchase"
```

Do not recompute project average order value from the customer export: it has no order-level key. Display the validated `average_order_value` from `project_kpis.csv`.

## 4. Build the worksheets

### 1. KPI strip

**Source:** `project_kpis.csv`

Create text cards for Clean Revenue, Customers, Completed Orders and Average Order Value. Keep this strip unfiltered because it is a one-row opening benchmark, not a filter-responsive transaction table.

Opening values:

| KPI | Expected |
|---|---:|
| Clean revenue | £8,911,407.90 |
| Customers | 4,338 |
| Completed orders | 18,532 |
| Average order value | £480.87 |

### 2. Segment overview

**Source:** `customer_segments.csv`

- Rows: `segment`
- Columns: Customers or Segment Revenue
- Label: Customers and Segment Revenue
- Sort: descending Segment Revenue
- Tooltip: segment, customers, revenue, average recency, average frequency and revenue per customer

Validate 947 Champions and 661 At Risk customers. Customer counts across all seven segments must total 4,338, and segment revenue must total £8,911,407.90.

### 3. RFM scatter

**Source:** `customer_segments.csv`

- Columns: `recency_days`
- Rows: `monetary`
- Detail: `customer_id`
- Size: `frequency`
- Colour: `segment`

Use transparency to reduce overplotting. State in the subtitle and tooltip that lower recency means a more recent purchase. Do not show `customer_id` in public labels or downloadable detail.

### 4. Segment profile

**Source:** `customer_segments.csv`

Show average Recency, Frequency and Monetary value by segment as separate aligned bars or a carefully labelled heatmap. Preserve each metric's units; do not place raw days, orders and currency on one unlabelled scale.

### 5. Country performance

**Source:** `country_performance.csv`

Use a ranked horizontal bar chart:

- Rows: `country`
- Columns: `revenue`
- Tooltip: country, customers, orders and revenue
- Sort: descending revenue

A ranked chart is preferred to a map when small countries or close values would be difficult to compare. Country revenue must total £8,911,407.90.

### 6. Monthly trend

**Source:** `monthly_revenue.csv`

- Columns: continuous `month`
- Rows: `revenue`
- Tooltip: month, customers, orders and revenue

Confirm chronological sorting and preserve the partial-period context of the source dates. Monthly revenue must total £8,911,407.90.

### 7. Product performance

**Source:** `product_performance.csv`

- Rows: `description`
- Columns: `revenue`
- Tooltip: stock code, description, units and revenue
- Filter: Top 10 by `SUM([revenue])`
- Sort: descending revenue

Keep `stock_code` in the tooltip so duplicate or similar descriptions remain distinguishable. Product revenue must total £8,911,407.90 before the Top 10 filter.

## 5. Dashboard layout

Use a desktop canvas near 1200 × 850 pixels:

1. Title, source/licence note and refresh context
2. Fixed opening KPI strip
3. Segment overview and RFM scatter
4. Segment profile
5. Country and monthly views
6. Product ranking
7. Filters, definitions and responsible-use note

Create a phone layout with KPI cards first, then Segment overview, RFM scatter, monthly trend and supporting rankings. Keep controls touch-friendly and avoid horizontal scrolling.

## 6. Filters and actions

Use source-scoped controls:

- Segment, R Score, F Score and M Score apply only to worksheets using `customer_segments.csv`.
- Country applies only to `country_performance.csv`.
- Product Top 10 applies only to `product_performance.csv`.
- Do not apply any dashboard filter to the fixed `project_kpis.csv` strip.

A Segment overview action may highlight or filter the RFM scatter and Segment profile because all three use the same customer source. Do not make it filter the country, month, product or fixed KPI worksheets; those exports contain no segment key.

Label the KPI strip **Overall validated totals** so viewers understand that source-scoped filters do not change it. Include a visible Revert All control.

## 7. Tooltips and responsible interpretation

- Define Recency, Frequency and Monetary in plain language.
- Pair every revenue value with customer or order context where the source provides it.
- Describe segments as historical transaction groupings, not personal characteristics.
- Avoid claims that a segment guarantees future behaviour.
- Frame recommendations as testable campaigns with measurement and opt-out safeguards.
- Do not expose customer identifiers in marks, screenshots or downloadable detail.

## 8. Accessibility

- Use a colour-blind-safe palette and do not encode segment only by colour.
- Maintain strong text/background contrast.
- Use descriptive worksheet titles and Tableau alt text.
- Keep keyboard reading order aligned with the dashboard layout.
- Test labels, tooltips and controls at 200% zoom.
- Check desktop and phone layouts for clipped text and overlapping marks.

## 9. Publication gate

Complete every item in [`VALIDATION_CHECKLIST.md`](VALIDATION_CHECKLIST.md) before publication. In particular:

- reconcile all opening KPIs and segment counts;
- prove that month, country and product revenue each independently match the validated total;
- test only source-compatible filters and actions;
- verify that customer identifiers cannot be downloaded;
- capture desktop and phone evidence; and
- open the Tableau Public link signed out before adding it to the README or either portfolio.

If any required check fails, keep the project marked **Tableau pending**.
