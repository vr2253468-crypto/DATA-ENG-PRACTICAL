from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


DATASETS = ("customers", "products", "orders", "payments")
REQUIRED_COLUMNS = {
    "customers": ("customer_id", "email", "country", "updated_at"),
    "products": ("product_id", "product_name", "category", "unit_price", "updated_at"),
    "orders": ("order_id", "customer_id", "product_id", "quantity", "order_status", "order_date", "updated_at"),
    "payments": ("payment_id", "order_id", "payment_method", "payment_status", "amount", "updated_at"),
}


SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY, email TEXT NOT NULL, country TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY, product_name TEXT NOT NULL, category TEXT NOT NULL,
    unit_price REAL NOT NULL CHECK (unit_price >= 0), updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY, customer_id TEXT NOT NULL, product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0), order_status TEXT NOT NULL,
    order_date TEXT NOT NULL, updated_at TEXT NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);
CREATE TABLE IF NOT EXISTS payments (
    payment_id TEXT PRIMARY KEY, order_id TEXT NOT NULL, payment_method TEXT NOT NULL,
    payment_status TEXT NOT NULL, amount REAL NOT NULL CHECK (amount >= 0), updated_at TEXT NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(order_id)
);
CREATE TABLE IF NOT EXISTS pipeline_state (
    dataset TEXT PRIMARY KEY, watermark TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ingestion_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT, started_at TEXT NOT NULL,
    finished_at TEXT NOT NULL, mode TEXT NOT NULL, rows_read INTEGER NOT NULL,
    rows_loaded INTEGER NOT NULL, issues_found INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS data_quality_issues (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT, run_id INTEGER NOT NULL,
    dataset TEXT NOT NULL, row_key TEXT, issue TEXT NOT NULL,
    FOREIGN KEY(run_id) REFERENCES ingestion_runs(run_id)
);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_and_clean(dataset: str, path: Path) -> tuple[pd.DataFrame, list[tuple[str | None, str]]]:
    issues: list[tuple[str | None, str]] = []
    if not path.exists():
        raise FileNotFoundError(f"Missing required input: {path}")
    frame = pd.read_csv(path)
    missing = [column for column in REQUIRED_COLUMNS[dataset] if column not in frame.columns]
    if missing:
        raise ValueError(f"{path.name} is missing columns: {', '.join(missing)}")

    frame = frame.drop_duplicates(keep="last").copy()
    frame["updated_at"] = pd.to_datetime(frame["updated_at"], errors="coerce", utc=True)
    invalid_dates = frame["updated_at"].isna()
    for key in frame.loc[invalid_dates, REQUIRED_COLUMNS[dataset][0]].astype(str):
        issues.append((key, "invalid updated_at"))
    frame = frame.loc[~invalid_dates].copy()

    key_column = REQUIRED_COLUMNS[dataset][0]
    frame[key_column] = frame[key_column].astype("string").str.strip()
    blank_keys = frame[key_column].isna() | frame[key_column].eq("")
    for index in frame.index[blank_keys]:
        issues.append((str(index), f"blank {key_column}"))
    frame = frame.loc[~blank_keys].copy()
    frame = frame.sort_values("updated_at").drop_duplicates(key_column, keep="last")

    for column in ("email", "country", "product_name", "category", "order_status", "payment_method", "payment_status"):
        if column in frame:
            frame[column] = frame[column].astype("string").str.strip()
    for column in ("unit_price", "amount"):
        if column in frame:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if "quantity" in frame:
        frame["quantity"] = pd.to_numeric(frame["quantity"], errors="coerce")
    if "order_date" in frame:
        frame["order_date"] = pd.to_datetime(frame["order_date"], errors="coerce", utc=True)

    if dataset == "customers":
        validation_rules = [("email", frame["email"].isna()), ("country", frame["country"].isna())]
    elif dataset == "products":
        validation_rules = [("unit_price", frame["unit_price"].isna() | (frame["unit_price"] < 0))]
    elif dataset == "orders":
        validation_rules = [("quantity", frame["quantity"].isna() | (frame["quantity"] <= 0)),
                            ("order_date", frame["order_date"].isna())]
    else:
        validation_rules = [("amount", frame["amount"].isna() | (frame["amount"] < 0))]
    for column, invalid in validation_rules:
        for key in frame.loc[invalid, key_column].astype(str):
            issues.append((key, f"invalid {column}"))
    invalid_rows = pd.Series(False, index=frame.index)
    for _, invalid in validation_rules:
        invalid_rows |= invalid
    return frame.loc[~invalid_rows].copy(), issues


def upsert_frame(connection: sqlite3.Connection, dataset: str, frame: pd.DataFrame) -> None:
    columns = list(frame.columns)
    frame = frame.copy()
    for column in ("updated_at", "order_date"):
        if column in frame:
            frame[column] = frame[column].map(lambda value: value.isoformat() if pd.notna(value) else None)
    frame = frame.where(pd.notna(frame), None)
    placeholders = ", ".join("?" for _ in columns)
    assignments = ", ".join(f"{column}=excluded.{column}" for column in columns[1:])
    sql = (f"INSERT INTO {dataset} ({', '.join(columns)}) VALUES ({placeholders}) "
           f"ON CONFLICT({columns[0]}) DO UPDATE SET {assignments}")
    connection.executemany(sql, frame[columns].itertuples(index=False, name=None))


def build_report(connection: sqlite3.Connection, report_path: Path) -> int:
    query = """
    SELECT substr(o.order_date, 1, 7) AS month, c.country, p.category,
           COUNT(DISTINCT o.order_id) AS orders,
           SUM(o.quantity) AS units,
           ROUND(SUM(o.quantity * p.unit_price), 2) AS gross_sales,
           ROUND(SUM(CASE WHEN pay.payment_status = 'paid' THEN pay.amount ELSE 0 END), 2) AS paid_amount
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    JOIN products p ON p.product_id = o.product_id
    LEFT JOIN payments pay ON pay.order_id = o.order_id
    WHERE o.order_status <> 'cancelled'
    GROUP BY month, c.country, p.category
    ORDER BY month, c.country, p.category
    """
    report = pd.read_sql_query(query, connection)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(report_path, index=False)
    return len(report)


def run_pipeline(input_dir: Path, db_path: Path, report_path: Path) -> dict[str, Any]:
    started_at = utc_now()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SCHEMA)
    watermarks = dict(connection.execute("SELECT dataset, watermark FROM pipeline_state"))
    mode = "incremental" if watermarks else "historical"
    rows_read = rows_loaded = issues_found = 0
    pending_issues: list[tuple[str, str | None, str]] = []

    try:
        for dataset in DATASETS:
            frame, issues = read_and_clean(dataset, input_dir / f"{dataset}.csv")
            rows_read += len(frame) + len(issues)
            for key, issue in issues:
                pending_issues.append((dataset, key, issue))
            watermark = watermarks.get(dataset)
            if watermark:
                frame = frame.loc[frame["updated_at"].map(lambda value: value.isoformat()) > watermark]
            if dataset == "orders" and not frame.empty:
                customer_ids = {row[0] for row in connection.execute("SELECT customer_id FROM customers")}
                product_ids = {row[0] for row in connection.execute("SELECT product_id FROM products")}
                missing_customer = ~frame["customer_id"].isin(customer_ids)
                missing_product = ~frame["product_id"].isin(product_ids)
                for key in frame.loc[missing_customer, "order_id"].astype(str):
                    pending_issues.append((dataset, key, "unknown customer_id"))
                for key in frame.loc[missing_product, "order_id"].astype(str):
                    pending_issues.append((dataset, key, "unknown product_id"))
                frame = frame.loc[~(missing_customer | missing_product)].copy()
            if dataset == "payments" and not frame.empty:
                order_ids = {row[0] for row in connection.execute("SELECT order_id FROM orders")}
                missing_order = ~frame["order_id"].isin(order_ids)
                for key in frame.loc[missing_order, "payment_id"].astype(str):
                    pending_issues.append((dataset, key, "unknown order_id"))
                frame = frame.loc[~missing_order].copy()
            if not frame.empty:
                upsert_frame(connection, dataset, frame)
                rows_loaded += len(frame)
            if not frame.empty:
                latest = frame["updated_at"].max().isoformat()
                connection.execute("INSERT INTO pipeline_state(dataset, watermark) VALUES (?, ?) "
                                   "ON CONFLICT(dataset) DO UPDATE SET watermark=excluded.watermark",
                                   (dataset, latest))

        report_rows = build_report(connection, report_path)
        finished_at = utc_now()
        cursor = connection.execute(
            "INSERT INTO ingestion_runs(started_at, finished_at, mode, rows_read, rows_loaded, issues_found) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (started_at, finished_at, mode, rows_read, rows_loaded, len(pending_issues)),
        )
        run_id = cursor.lastrowid
        connection.executemany(
            "INSERT INTO data_quality_issues(run_id, dataset, row_key, issue) VALUES (?, ?, ?, ?)",
            [(run_id, dataset, key, issue) for dataset, key, issue in pending_issues],
        )
        connection.commit()
        return {"mode": mode, "rows_read": rows_read, "rows_loaded": rows_loaded,
                "issues": len(pending_issues), "report_rows": report_rows}
    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="CSV to Pandas to SQLite e-commerce ETL pipeline")
    parser.add_argument("--input-dir", type=Path, default=Path("data"))
    parser.add_argument("--db", type=Path, default=Path("warehouse/ecommerce.db"))
    parser.add_argument("--report", type=Path, default=Path("reports/sales_report.csv"))
    args = parser.parse_args()
    result = run_pipeline(args.input_dir, args.db, args.report)
    print("ETL complete:", ", ".join(f"{key}={value}" for key, value in result.items()))


if __name__ == "__main__":
    main()
