# Data

## File

The complete `online_retail_clean.csv.gz` dataset contains 397,884 valid sales lines and nine columns. It is stored as ten numbered parts, while `online_retail_sample.csv` provides the first 500 rows for browser preview.

Reconstruct and decompress the full CSV:

```bash
cat online_retail_clean.csv.gz.part-* > online_retail_clean.csv.gz
gzip -dk online_retail_clean.csv.gz
```

## Source

- Dataset: UCI Online Retail
- URL: https://archive.ics.uci.edu/dataset/352/online+retail
- DOI: https://doi.org/10.24432/C5BW33
- Creator: Daqing Chen
- License: CC BY 4.0

## Preparation

The source `Online Retail.xlsx` workbook was filtered to retain rows with a customer ID, positive quantity, positive unit price and an invoice number that does not begin with `C`. `Revenue` equals `Quantity * UnitPrice`, and dates use `YYYY-MM-DD HH:MM:SS`.

## Validation

| Check | Result |
|---|---:|
| Valid sales rows | 397,884 |
| Customers | 4,338 |
| Completed orders | 18,532 |
| Clean revenue | £8,911,407.90 |
| Average order value | £480.87 |

Uncompressed CSV SHA-256: `3bb3383de1bc05e9094e29d47a597ed864069139586bb2e339e9bc035584ffdc`

Compressed file SHA-256: `b2e22f4e237c59f5266681a45274ab7e6dd4232b88e2d62781cb73c29eef8d3b`
