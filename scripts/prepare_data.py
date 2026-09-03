#!/usr/bin/env python3
"""Rebuild and validate the cleaned UCI Online Retail transaction file."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover - dependency guidance for CLI users
    raise SystemExit(
        "This script requires pandas and openpyxl: "
        "python3 -m pip install pandas openpyxl"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]
OUTPUT_COLUMNS = [*EXPECTED_COLUMNS, "Revenue"]
EXPECTED_ROWS = 397_884
EXPECTED_CUSTOMERS = 4_338
EXPECTED_ORDERS = 18_532
EXPECTED_REVENUE = 8_911_407.90
EXPECTED_AVERAGE_ORDER_VALUE = 480.87
EXPECTED_SHA256 = "3bb3383de1bc05e9094e29d47a597ed864069139586bb2e339e9bc035584ffdc"


def prepare(source: Path) -> pd.DataFrame:
    """Apply the documented cleaning rules while preserving source row order."""
    frame = pd.read_excel(source, engine="openpyxl")
    missing = [column for column in EXPECTED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Source workbook is missing columns: {', '.join(missing)}")

    frame = frame[EXPECTED_COLUMNS].copy()
    frame = frame[
        frame["CustomerID"].notna()
        & ~frame["InvoiceNo"].astype(str).str.startswith("C")
        & frame["Quantity"].gt(0)
        & frame["UnitPrice"].gt(0)
    ].copy()

    frame["InvoiceNo"] = frame["InvoiceNo"].astype(str)
    frame["StockCode"] = frame["StockCode"].astype(str)
    frame["InvoiceDate"] = pd.to_datetime(frame["InvoiceDate"]).dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    frame["CustomerID"] = frame["CustomerID"].astype("int64").astype(str)
    frame["Revenue"] = frame["Quantity"] * frame["UnitPrice"]
    return frame[OUTPUT_COLUMNS]


def validate(frame: pd.DataFrame) -> None:
    """Fail before writing when the documented project KPIs do not reconcile."""
    orders = frame["InvoiceNo"].nunique()
    checks = {
        "rows": (len(frame), EXPECTED_ROWS),
        "customers": (frame["CustomerID"].nunique(), EXPECTED_CUSTOMERS),
        "orders": (orders, EXPECTED_ORDERS),
        "revenue": (round(frame["Revenue"].sum(), 2), EXPECTED_REVENUE),
        "average order value": (
            round(frame["Revenue"].sum() / orders, 2),
            EXPECTED_AVERAGE_ORDER_VALUE,
        ),
    }
    failures = [
        f"{name}: expected {expected!r}, got {actual!r}"
        for name, (actual, expected) in checks.items()
        if actual != expected
    ]
    if failures:
        raise ValueError("Validation failed:\n- " + "\n- ".join(failures))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare the UCI Online Retail workbook for this project."
    )
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=ROOT / "data" / "Online Retail.xlsx",
        help="source workbook (default: data/Online Retail.xlsx)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "online_retail_clean.csv",
        help="clean CSV destination (default: data/online_retail_clean.csv)",
    )
    args = parser.parse_args()

    frame = prepare(args.source.resolve())
    validate(frame)

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    frame.to_csv(temporary, index=False, lineterminator="\n")
    digest = sha256(temporary)
    if digest != EXPECTED_SHA256:
        temporary.unlink(missing_ok=True)
        raise ValueError(
            f"Output SHA-256 mismatch: expected {EXPECTED_SHA256}, got {digest}"
        )
    os.replace(temporary, output)

    print(f"Prepared {len(frame):,} valid sales rows in {output}.")
    print(f"Customers: {frame['CustomerID'].nunique():,}")
    print(f"Orders: {frame['InvoiceNo'].nunique():,}")
    print(f"Revenue: £{frame['Revenue'].sum():,.2f}")
    print(f"SHA-256: {digest}")


if __name__ == "__main__":
    main()
