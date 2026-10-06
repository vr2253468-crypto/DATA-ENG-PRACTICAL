from pathlib import Path

import pandas as pd


EXPECTED_FILES = ("customers.csv", "products.csv", "orders.csv", "payments.csv")


def read_source_data(data_dir: Path) -> dict[str, pd.DataFrame]:
    """Extract the four source tables from CSV files."""
    tables = {}
    for filename in EXPECTED_FILES:
        path = data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing source file: {path}")
        tables[path.stem] = pd.read_csv(path, dtype=str)
    return tables
