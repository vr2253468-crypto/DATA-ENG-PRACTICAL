from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


SCHEMA = """
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT NOT NULL UNIQUE, customer_name TEXT NOT NULL,
    gender TEXT NOT NULL, city TEXT NOT NULL, registration_date TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS dim_product (
    product_key INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL UNIQUE, product_name TEXT NOT NULL,
    category TEXT NOT NULL, price REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY, full_date TEXT NOT NULL UNIQUE,
    day INTEGER NOT NULL, month INTEGER NOT NULL, quarter INTEGER NOT NULL, year INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS dim_payment (
    payment_key INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_id TEXT NOT NULL UNIQUE, payment_method TEXT NOT NULL, payment_status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS fact_sales (
    sales_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL UNIQUE, customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL, date_key INTEGER NOT NULL, payment_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL, sales_amount REAL NOT NULL,
    FOREIGN KEY(customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY(product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY(date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY(payment_key) REFERENCES dim_payment(payment_key)
);
"""


def load_star_schema(sales: pd.DataFrame, database_path: Path) -> int:
    """Upsert dimensions and facts; order_id makes repeated runs idempotent."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    try:
        connection.executescript(SCHEMA)
        for row in sales[["customer_id", "customer_name", "gender", "city", "registration_date"]].drop_duplicates("customer_id").itertuples(index=False):
            connection.execute("""INSERT INTO dim_customer(customer_id, customer_name, gender, city, registration_date)
                VALUES (?, ?, ?, ?, ?) ON CONFLICT(customer_id) DO UPDATE SET customer_name=excluded.customer_name,
                gender=excluded.gender, city=excluded.city, registration_date=excluded.registration_date""", tuple(row))
        for row in sales[["product_id", "product_name", "category", "price"]].drop_duplicates("product_id").itertuples(index=False):
            connection.execute("""INSERT INTO dim_product(product_id, product_name, category, price)
                VALUES (?, ?, ?, ?) ON CONFLICT(product_id) DO UPDATE SET product_name=excluded.product_name,
                category=excluded.category, price=excluded.price""", tuple(row))
        for row in sales[["order_date"]].drop_duplicates().itertuples(index=False):
            date = pd.Timestamp(row.order_date)
            connection.execute("INSERT OR IGNORE INTO dim_date VALUES (?, ?, ?, ?, ?, ?)",
                (int(date.strftime("%Y%m%d")), date.strftime("%Y-%m-%d"), date.day, date.month,
                 (date.month - 1) // 3 + 1, date.year))
        for row in sales[["payment_id", "payment_method", "payment_status"]].drop_duplicates("payment_id").itertuples(index=False):
            connection.execute("""INSERT INTO dim_payment(payment_id, payment_method, payment_status)
                VALUES (?, ?, ?) ON CONFLICT(payment_id) DO UPDATE SET payment_method=excluded.payment_method,
                payment_status=excluded.payment_status""", tuple(row))

        customer_keys = dict(connection.execute("SELECT customer_id, customer_key FROM dim_customer"))
        product_keys = dict(connection.execute("SELECT product_id, product_key FROM dim_product"))
        payment_keys = dict(connection.execute("SELECT payment_id, payment_key FROM dim_payment"))
        for row in sales.itertuples(index=False):
            date = pd.Timestamp(row.order_date)
            connection.execute("""INSERT INTO fact_sales(order_id, customer_key, product_key, date_key,
                payment_key, quantity, sales_amount) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(order_id) DO UPDATE SET customer_key=excluded.customer_key,
                product_key=excluded.product_key, date_key=excluded.date_key,
                payment_key=excluded.payment_key, quantity=excluded.quantity, sales_amount=excluded.sales_amount""",
                (row.order_id, customer_keys[row.customer_id], product_keys[row.product_id],
                 int(date.strftime("%Y%m%d")), payment_keys[row.payment_id], row.quantity, row.total_amount))
        connection.commit()
        return connection.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0]
    finally:
        connection.close()
