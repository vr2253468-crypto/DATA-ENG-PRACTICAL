import csv
import sqlite3
import tempfile
import unittest
from pathlib import Path

from etl_pipeline import run_pipeline


class PipelineTest(unittest.TestCase):
    def write_inputs(self, directory: Path, order_status: str = "completed") -> None:
        files = {
            "customers.csv": "customer_id,email,country,updated_at\nC1,test@example.com,India,2026-01-01T00:00:00Z\n",
            "products.csv": "product_id,product_name,category,unit_price,updated_at\nP1,Test Product,Test,10.00,2026-01-01T00:00:00Z\n",
            "orders.csv": f"order_id,customer_id,product_id,quantity,order_status,order_date,updated_at\nO1,C1,P1,2,{order_status},2026-01-02T00:00:00Z,2026-01-02T00:00:00Z\n",
            "payments.csv": "payment_id,order_id,payment_method,payment_status,amount,updated_at\nPAY1,O1,card,paid,20.00,2026-01-02T00:01:00Z\n",
        }
        for name, content in files.items():
            (directory / name).write_text(content, encoding="utf-8")

    def test_historical_then_incremental_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_dir = root / "data"
            input_dir.mkdir()
            self.write_inputs(input_dir)
            db_path = root / "warehouse.db"
            report_path = root / "report.csv"

            first = run_pipeline(input_dir, db_path, report_path)
            self.assertEqual(first["mode"], "historical")
            self.assertEqual(first["rows_loaded"], 4)
            self.assertEqual(report_path.read_text(encoding="utf-8").count("\n"), 2)

            orders_path = input_dir / "orders.csv"
            orders_path.write_text(
                "order_id,customer_id,product_id,quantity,order_status,order_date,updated_at\n"
                "O1,C1,P1,3,completed,2026-01-02T00:00:00Z,2026-01-03T00:00:00Z\n",
                encoding="utf-8",
            )
            second = run_pipeline(input_dir, db_path, report_path)
            self.assertEqual(second["mode"], "incremental")
            self.assertEqual(second["rows_loaded"], 1)

            connection = sqlite3.connect(db_path)
            quantity = connection.execute("SELECT quantity FROM orders WHERE order_id = 'O1'").fetchone()[0]
            run_count = connection.execute("SELECT COUNT(*) FROM ingestion_runs").fetchone()[0]
            connection.close()
            self.assertEqual(quantity, 3)
            self.assertEqual(run_count, 2)

    def test_invalid_rows_are_logged_and_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            input_dir = root / "data"
            input_dir.mkdir()
            self.write_inputs(input_dir)
            (input_dir / "products.csv").write_text(
                "product_id,product_name,category,unit_price,updated_at\nP1,Test Product,Test,-1,2026-01-01T00:00:00Z\n",
                encoding="utf-8",
            )
            result = run_pipeline(input_dir, root / "warehouse.db", root / "report.csv")
            self.assertEqual(result["issues"], 3)
            connection = sqlite3.connect(root / "warehouse.db")
            product_count = connection.execute("SELECT COUNT(*) FROM products").fetchone()[0]
            issue_count = connection.execute("SELECT COUNT(*) FROM data_quality_issues").fetchone()[0]
            connection.close()
            self.assertEqual(product_count, 0)
            self.assertEqual(issue_count, 3)


if __name__ == "__main__":
    unittest.main()
