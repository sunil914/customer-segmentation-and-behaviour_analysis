#!/usr/bin/env python3
"""Export validated SQLite views as Tableau-ready CSV files."""

from __future__ import annotations

import argparse
import csv
import math
import os
import sqlite3
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPORTS = (
    ("v_project_kpis", ""),
    ("v_customer_segments", "ORDER BY customer_id"),
    ("v_monthly_revenue", "ORDER BY month"),
    ("v_country_performance", "ORDER BY country"),
    ("v_product_performance", "ORDER BY stock_code, description"),
)
EXPECTED_KPIS = {
    "line_items": 397_884,
    "customers": 4_338,
    "orders": 18_532,
    "revenue": 8_911_407.90,
    "average_order_value": 480.87,
}
EXPECTED_SEGMENTS = {"Champions": 947, "At Risk": 661}


def validate_database(connection: sqlite3.Connection) -> None:
    integrity = connection.execute("PRAGMA quick_check").fetchone()[0]
    if integrity != "ok":
        raise RuntimeError(f"SQLite integrity check failed: {integrity}")

    available = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'view'"
        )
    }
    missing = [view for view, _ in EXPORTS if view not in available]
    if missing:
        raise ValueError(f"Missing required views: {', '.join(missing)}")

    row = connection.execute("SELECT * FROM v_project_kpis").fetchone()
    if row is None:
        raise ValueError("v_project_kpis returned no data.")
    actual = dict(row)

    for key in ("line_items", "customers", "orders"):
        if actual[key] != EXPECTED_KPIS[key]:
            raise ValueError(
                f"{key} mismatch: expected {EXPECTED_KPIS[key]}, got {actual[key]}"
            )
    for key in ("revenue", "average_order_value"):
        if not math.isclose(
            actual[key], EXPECTED_KPIS[key], rel_tol=0, abs_tol=0.005
        ):
            raise ValueError(
                f"{key} mismatch: expected {EXPECTED_KPIS[key]}, got {actual[key]}"
            )

    segment_counts = dict(
        connection.execute(
            """
            SELECT segment, COUNT(*) AS customers
            FROM v_customer_segments
            GROUP BY segment
            """
        )
    )
    for segment, expected in EXPECTED_SEGMENTS.items():
        actual_count = segment_counts.get(segment)
        if actual_count != expected:
            raise ValueError(
                f"{segment} mismatch: expected {expected}, got {actual_count}"
            )


def export_view(
    connection: sqlite3.Connection,
    view: str,
    order_by: str,
    destination: Path,
) -> int:
    cursor = connection.execute(f'SELECT * FROM "{view}" {order_by}')
    headers = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    with destination.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate project.db and export Tableau-ready CSV files."
    )
    parser.add_argument(
        "--database",
        default=str(ROOT / "project.db"),
        help="SQLite database path (default: project.db in the repository root)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "tableau" / "exports"),
        help="CSV destination (default: tableau/exports)",
    )
    args = parser.parse_args()

    database = Path(args.database).resolve()
    output_dir = Path(args.output_dir).resolve()
    if not database.is_file():
        raise FileNotFoundError(
            f"{database} does not exist. Run scripts/build_database.py first."
        )

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row
        validate_database(connection)

        with tempfile.TemporaryDirectory(
            prefix="tableau-export-", dir=output_dir.parent
        ) as temporary:
            temporary_dir = Path(temporary)
            exported: list[tuple[str, int]] = []
            for view, order_by in EXPORTS:
                filename = f"{view.removeprefix('v_')}.csv"
                row_count = export_view(
                    connection, view, order_by, temporary_dir / filename
                )
                exported.append((filename, row_count))

            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, _ in exported:
                os.replace(temporary_dir / filename, output_dir / filename)

    for filename, row_count in exported:
        print(f"Exported {row_count:,} rows to {output_dir / filename}")


if __name__ == "__main__":
    main()
