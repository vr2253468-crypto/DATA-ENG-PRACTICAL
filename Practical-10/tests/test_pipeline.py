import sqlite3
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from scripts.cleaning import clean_data
from scripts.ingestion import read_source_data
from scripts.pipeline import run_pipeline


class PipelineTests(unittest.TestCase):
    def test_sample_pipeline_matches_expected_totals(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data_dir = root / "data"
            data_dir.mkdir()
            source = Path(__file__).parents[1] / "data"
            for filename in ("customers.csv", "products.csv", "orders.csv", "payments.csv"):
                (data_dir / filename).write_bytes((source / filename).read_bytes())
            result = run_pipeline(data_dir, root / "database" / "ecommerce.db", root / "output")
            self.assertEqual(result["loaded_rows"], 5)
            self.assertEqual(result["rejected_rows"], 0)
            connection = sqlite3.connect(root / "database" / "ecommerce.db")
            try:
                totals = connection.execute("SELECT SUM(sales_amount), COUNT(*), SUM(quantity) FROM fact_sales").fetchone()
                self.assertEqual(totals, (126000.0, 5, 9))
                dimensions = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                self.assertTrue({"fact_sales", "dim_customer", "dim_product", "dim_date", "dim_payment"}.issubset(dimensions))
            finally:
                connection.close()

    def test_invalid_quantity_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tables = {
                "customers": pd.DataFrame([{"customer_id": "C1", "customer_name": "A", "gender": "Male", "city": "Delhi", "registration_date": "2025-01-01"}]),
                "products": pd.DataFrame([{"product_id": "P1", "product_name": "Item", "category": "Tools", "price": "10"}]),
                "orders": pd.DataFrame([{"order_id": "O1", "customer_id": "C1", "product_id": "P1", "order_date": "2025-01-01", "quantity": "0", "payment_id": "PM1"}]),
                "payments": pd.DataFrame([{"payment_id": "PM1", "payment_method": "UPI", "payment_status": "Completed"}]),
            }
            cleaned, rejected = clean_data(tables)
            self.assertEqual(len(cleaned["orders"]), 0)
            self.assertEqual(len(rejected), 1)

    def test_new_order_is_upserted_without_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data_dir = root / "data"
            data_dir.mkdir()
            source = Path(__file__).parents[1] / "data"
            for filename in ("customers.csv", "products.csv", "orders.csv", "payments.csv"):
                (data_dir / filename).write_bytes((source / filename).read_bytes())
            database = root / "database" / "ecommerce.db"
            output = root / "output"
            run_pipeline(data_dir, database, output)
            orders = pd.read_csv(data_dir / "orders.csv")
            orders.loc[len(orders)] = ["O006", "C001", "P002", "2025-04-06", 1, "PM006"]
            payments = pd.read_csv(data_dir / "payments.csv")
            payments.loc[len(payments)] = ["PM006", "UPI", "Completed"]
            orders.to_csv(data_dir / "orders.csv", index=False)
            payments.to_csv(data_dir / "payments.csv", index=False)
            result = run_pipeline(data_dir, database, output)
            self.assertEqual(result["warehouse_rows"], 6)
            run_pipeline(data_dir, database, output)
            connection = sqlite3.connect(database)
            try:
                self.assertEqual(connection.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0], 6)
            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()
