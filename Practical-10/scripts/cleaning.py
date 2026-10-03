from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {
    "customers": {"customer_id", "customer_name", "gender", "city", "registration_date"},
    "products": {"product_id", "product_name", "category", "price"},
    "orders": {"order_id", "customer_id", "product_id", "order_date", "quantity", "payment_id"},
    "payments": {"payment_id", "payment_method", "payment_status"},
}


def clean_data(tables: dict[str, pd.DataFrame]) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Normalize values and remove invalid order records for safe loading."""
    cleaned: dict[str, pd.DataFrame] = {}
    for name, frame in tables.items():
        frame = frame.copy()
        frame.columns = frame.columns.str.strip().str.lower()
        missing = REQUIRED_COLUMNS[name] - set(frame.columns)
        if missing:
            raise ValueError(f"{name}.csv is missing columns: {sorted(missing)}")
        for column in frame.columns:
            frame[column] = frame[column].fillna("").astype(str).str.strip()
        cleaned[name] = frame.drop_duplicates().reset_index(drop=True)

    customers = cleaned["customers"]
    products = cleaned["products"]
    orders = cleaned["orders"]
    payments = cleaned["payments"]
    customers["registration_date"] = pd.to_datetime(customers["registration_date"], errors="coerce")
    products["price"] = pd.to_numeric(products["price"], errors="coerce")
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    orders["quantity"] = pd.to_numeric(orders["quantity"], errors="coerce")

    valid = (
        orders["order_id"].ne("")
        & orders["customer_id"].ne("")
        & orders["product_id"].ne("")
        & orders["payment_id"].ne("")
        & orders["order_date"].notna()
        & orders["quantity"].gt(0)
        & orders["quantity"].mod(1).eq(0)
        & orders["customer_id"].isin(customers["customer_id"])
        & orders["product_id"].isin(products["product_id"])
        & orders["payment_id"].isin(payments["payment_id"])
    )
    rejected = orders.loc[~valid].copy()
    rejected["rejection_reason"] = "missing reference, invalid date, or non-positive quantity"
    cleaned["orders"] = orders.loc[valid].drop_duplicates("order_id", keep="last").copy()
    cleaned["orders"]["quantity"] = cleaned["orders"]["quantity"].astype(int)
    cleaned["products"] = products.loc[products["price"].gt(0)].copy()
    cleaned["customers"] = customers.loc[customers["registration_date"].notna()].copy()
    cleaned["customers"]["registration_date"] = cleaned["customers"]["registration_date"].dt.strftime("%Y-%m-%d")
    return cleaned, rejected
