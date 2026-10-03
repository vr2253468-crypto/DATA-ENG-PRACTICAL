from __future__ import annotations

import html
import sqlite3
from pathlib import Path

import pandas as pd

from .cleaning import clean_data
from .ingestion import read_source_data
from .load_database import load_star_schema
from .transformation import transform_data

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
DATABASE_PATH = ROOT / "database" / "ecommerce.db"

QUERIES = {
    "sales_by_category.csv": "SELECT p.category, ROUND(SUM(f.sales_amount), 2) AS total_sales FROM fact_sales f JOIN dim_product p ON f.product_key=p.product_key GROUP BY p.category ORDER BY total_sales DESC",
    "sales_by_product.csv": "SELECT p.product_name, ROUND(SUM(f.sales_amount), 2) AS total_sales FROM fact_sales f JOIN dim_product p ON f.product_key=p.product_key GROUP BY p.product_name ORDER BY total_sales DESC",
    "sales_by_city.csv": "SELECT c.city, ROUND(SUM(f.sales_amount), 2) AS total_sales FROM fact_sales f JOIN dim_customer c ON f.customer_key=c.customer_key GROUP BY c.city ORDER BY total_sales DESC",
    "monthly_sales.csv": "SELECT d.year, d.month, ROUND(SUM(f.sales_amount), 2) AS monthly_sales FROM fact_sales f JOIN dim_date d ON f.date_key=d.date_key GROUP BY d.year, d.month ORDER BY d.year, d.month",
    "payment_method_distribution.csv": "SELECT p.payment_method, COUNT(*) AS orders, ROUND(SUM(f.sales_amount), 2) AS total_sales FROM fact_sales f JOIN dim_payment p ON f.payment_key=p.payment_key GROUP BY p.payment_method ORDER BY total_sales DESC",
}


def generate_reports(database_path: Path, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    reports: dict[str, Path] = {}
    connection = sqlite3.connect(database_path)
    try:
        summary = pd.read_sql_query("SELECT COALESCE(SUM(sales_amount),0) total_sales, COUNT(*) total_orders, COALESCE(SUM(quantity),0) total_quantity FROM fact_sales", connection).iloc[0]
        sections = []
        for filename, query in QUERIES.items():
            frame = pd.read_sql_query(query, connection)
            path = output_dir / filename
            frame.to_csv(path, index=False)
            reports[filename] = path
            sections.append(f"<section><h2>{html.escape(filename.replace('.csv', '').replace('_', ' ').title())}</h2>{frame.to_html(index=False, classes='report-table')}</section>")
        sales = pd.read_sql_query("SELECT * FROM fact_sales", connection)
        sales.to_csv(output_dir / "cleaned_sales.csv", index=False)
        reports["cleaned_sales.csv"] = output_dir / "cleaned_sales.csv"
    finally:
        connection.close()
    average = summary.total_sales / summary.total_orders if summary.total_orders else 0
    cards = "".join(f"<article><strong>{value}</strong><span>{label}</span></article>" for label, value in [("Total Sales", f"₹{summary.total_sales:,.0f}"), ("Total Orders", int(summary.total_orders)), ("Total Quantity", int(summary.total_quantity)), ("Average Order Value", f"₹{average:,.0f}")])
    dashboard = output_dir / "dashboard.html"
    dashboard.write_text(f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>E-Commerce Sales Dashboard</title><style>body{{font:16px Georgia,serif;max-width:1150px;margin:32px auto;padding:0 18px;color:#17324d;background:#f4f1ea}}h1{{font-size:40px;margin-bottom:4px}}p{{color:#537087}}.cards{{display:flex;gap:14px;flex-wrap:wrap;margin:25px 0}}article{{background:#fff;border-left:5px solid #e26d5a;padding:16px 22px;min-width:160px;box-shadow:0 3px 12px #17324d18}}article strong,article span{{display:block}}article strong{{font-size:25px}}article span{{margin-top:7px;color:#537087}}section{{background:#fff;padding:18px;margin:20px 0;overflow:auto;box-shadow:0 3px 12px #17324d12}}h2{{margin-top:0;color:#e26d5a}}table{{border-collapse:collapse;width:100%}}th,td{{padding:8px 11px;border-bottom:1px solid #dce3e6;text-align:left}}th{{background:#e8eef0}}</style></head><body><h1>E-Commerce Sales Dashboard</h1><p>Star-schema analytics refreshed from the CSV source tables.</p><div class='cards'>{cards}</div>{''.join(sections)}</body></html>""", encoding="utf-8")
    reports["dashboard.html"] = dashboard
    return reports


def run_pipeline(data_dir: Path = DATA_DIR, database_path: Path = DATABASE_PATH, output_dir: Path = OUTPUT_DIR) -> dict[str, object]:
    print("Starting ETL Pipeline...")
    print("1. Extracting data...")
    raw = read_source_data(data_dir)
    print("2. Cleaning data...")
    cleaned, rejected = clean_data(raw)
    output_dir.mkdir(parents=True, exist_ok=True)
    rejected.to_csv(output_dir / "rejected_orders.csv", index=False)
    print("3. Transforming data...")
    sales = transform_data(cleaned)
    print("4. Loading data warehouse...")
    warehouse_rows = load_star_schema(sales, database_path)
    print("5. Generating reports...")
    reports = generate_reports(database_path, output_dir)
    print("ETL Pipeline Completed Successfully!")
    return {"loaded_rows": len(sales), "rejected_rows": len(rejected), "warehouse_rows": warehouse_rows, "database": database_path, "reports": reports}


if __name__ == "__main__":
    run_pipeline()
