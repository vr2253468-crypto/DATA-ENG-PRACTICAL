from __future__ import annotations

import pandas as pd


def transform_data(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Join source tables and calculate the sales amount."""
    sales = tables["orders"].merge(tables["customers"], on="customer_id", how="left")
    sales = sales.merge(tables["products"], on="product_id", how="left")
    sales = sales.merge(tables["payments"], on="payment_id", how="left")
    sales["total_amount"] = sales["quantity"] * sales["price"]
    return sales
