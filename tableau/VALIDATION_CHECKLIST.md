# Tableau Validation Checklist

> **Status:** Pre-publication quality-assurance specification. The Tableau workbook, screenshots and Tableau Public link are still pending.

Use this checklist after running:

```bash
python3 scripts/build_database.py
python3 scripts/export_tableau_data.py
```

The exporter must finish without an integrity, KPI or segment error before Tableau testing begins. Connect only the five CSV files in `tableau/exports/`.

## 1. Source and schema checks

- [ ] `project_kpis.csv` loads as a single KPI row.
- [ ] `customer_segments.csv` keeps `customer_id` as text, not a number.
- [ ] Revenue and Monetary fields are decimal measures formatted as GBP.
- [ ] Month is parsed as a chronological date, not sorted alphabetically.
- [ ] Each worksheet uses the export named in the build guide; no manual aggregate is joined back to customer-level data.
- [ ] Lower Recency is explained as a more recent purchase in the RFM scatter tooltip.

## 2. Opening reconciliation

With every dashboard filter cleared, record Tableau's displayed result and compare it with the validated source.

| Check | Expected result | Pass condition |
|---|---:|---|
| Valid sales lines | 397,884 | Exact |
| Customers | 4,338 | Exact distinct count |
| Completed orders | 18,532 | Exact distinct count |
| Clean revenue | £8,911,407.90 | Equal to the penny |
| Average order value | £480.87 | Equal after two-decimal display rounding |
| Champions | 947 | Exact customer count |
| At Risk | 661 | Exact customer count |

- [ ] Segment customer counts sum to 4,338.
- [ ] Segment revenue sums to £8,911,407.90.
- [ ] Country, month and product revenue each independently reconcile to £8,911,407.90.
- [ ] KPI cards return to the opening values after **Revert All** or clearing filters.

## 3. Interaction tests

- [ ] Segment and Country filters affect only worksheets with compatible fields.
- [ ] Selecting a segment highlights the intended customers without changing unrelated totals.
- [ ] Multi-select, single-select and clear-filter actions give predictable results.
- [ ] Empty selections show an explanatory state instead of a misleading zero.
- [ ] Top 10 Product Performance responds correctly to compatible filters.
- [ ] Tooltips show the active segment or country context and define each metric.

## 4. Visual and accessibility checks

- [ ] Important values have text labels and do not rely on colour alone.
- [ ] The palette remains distinguishable for common colour-vision deficiencies.
- [ ] Text and marks have sufficient contrast against their backgrounds.
- [ ] Worksheet titles describe the measure and grouping in plain language.
- [ ] Reading and tab order follow KPI strip → segment views → supporting views.
- [ ] Desktop layout has no clipped labels, overlapping marks or horizontal scrolling.
- [ ] Phone layout keeps KPIs first, uses touch-friendly controls and avoids tiny legends.
- [ ] Decorative elements do not obscure data or keyboard focus.

## 5. Responsible-use and publication gate

- [ ] Customer IDs appear only where analytically necessary and are excluded from public labels, screenshots and downloadable detail.
- [ ] RFM segments are described as historical behaviour, not personal traits or guaranteed future actions.
- [ ] Recommendations are framed as testable marketing actions, not deterministic decisions.
- [ ] Workbook title, source, licence, refresh date and analytical limitations are visible.
- [ ] Desktop and phone screenshots match the final published workbook.
- [ ] The repository receives the workbook or documented workbook source, screenshots and Tableau Public URL only after every required check passes.

Do not mark the Tableau dashboard complete until the opening reconciliation, interaction, accessibility and responsible-use sections all pass.
