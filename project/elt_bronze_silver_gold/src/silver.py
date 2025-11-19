# silver.py

import numpy as np
import pandas as pd

from .config import BRONZE, SILVER
from .io_utils import reset_dir, write_parquet


def parse_mixed_ts(x: str) -> pd.Timestamp:
    if pd.isna(x):
        return pd.NaT
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%d-%m-%Y %H:%M:%S", "%Y-%m-%d"):
        try:
            return pd.to_datetime(x, format=fmt, utc=True)
        except Exception:
            continue
    return pd.to_datetime(x, utc=True, errors="coerce")


def parse_money(x: str) -> float:
    if pd.isna(x):
        return np.nan
    x = str(x).replace(",", ".").strip()
    try:
        return float(x)
    except Exception:
        return np.nan


def silver_transform() -> None:
    reset_dir(SILVER)

    # ---------------------------
    # Customers -> dim_customer
    # ---------------------------
    customers = pd.read_csv(
        BRONZE / "customers.csv",
        dtype={"customer_id": "Int64", "email": "string", "country": "string", "signup_ts": "string"},
    )
    customers = customers.drop_duplicates(subset=["customer_id"], keep="last")
    customers["signup_ts"] = customers["signup_ts"].map(parse_mixed_ts)
    customers["country"] = customers["country"].fillna("UNK").str.upper().str.strip()
    customers["email"] = customers["email"].str.lower().str.strip()
    write_parquet(customers, SILVER / "dim_customer.parquet")

    # ---------------------------
    # Products -> dim_product
    # ---------------------------
    products = pd.read_json(
        BRONZE / "products.jsonl",
        lines=True,
        dtype={
            "product_id": "Int64",
            "sku": "string",
            "name": "string",
            "category": "string",
            "unit_price": "float",
            "active": "boolean",
        },
    )
    products["category"] = products["category"].str.upper()
    write_parquet(products, SILVER / "dim_product.parquet")

    # ---------------------------
    # Orders (typed)
    # ---------------------------
    orders = pd.read_csv(
        BRONZE / "orders.csv",
        dtype={
            "order_id": "Int64",
            "customer_id": "Int64",
            "order_ts": "string",
            "status": "string",
            "currency": "string",
            "order_total": "string",
        },
    )
    orders["order_ts"] = orders["order_ts"].map(parse_mixed_ts)
    orders["status"] = orders["status"].str.lower().str.strip()
    orders["currency"] = orders["currency"].str.upper().str.strip()
    # keep raw order_total for now; we will recompute from items

    # ---------------------------
    # Order items (typed)
    # ---------------------------
    order_items = pd.read_csv(
        BRONZE / "order_items.csv",
        dtype={"order_id": "Int64", "product_id": "Int64", "qty": "Int64", "unit_price": "string"},
    )
    order_items["unit_price"] = order_items["unit_price"].map(parse_money)
    order_items = order_items.dropna(subset=["unit_price"])

    # ---------------------------
    # QA reports (pre-enforcement)
    # ---------------------------
    bad_orders = orders.merge(customers[["customer_id"]], on="customer_id", how="left", indicator=True)
    bad_orders = bad_orders[bad_orders["_merge"] == "left_only"][["order_id", "customer_id"]]
    write_parquet(bad_orders, SILVER / "qa_bad_orders_missing_customer.parquet")

    bad_items = order_items.merge(products[["product_id"]], on="product_id", how="left", indicator=True)
    bad_items = bad_items[bad_items["_merge"] == "left_only"][["order_id", "product_id"]]
    write_parquet(bad_items, SILVER / "qa_bad_items_missing_product.parquet")

    # ---------------------------
    # Enforce referential integrity in Silver outputs
    # ---------------------------
    orders = orders[orders["customer_id"].isin(customers["customer_id"])]
    order_items = order_items[order_items["product_id"].isin(products["product_id"])]

    # Optional: keep only items whose order_id exists after customer filtering
    order_items = order_items[order_items["order_id"].isin(orders["order_id"])]

    # ---------------------------
    # Recompute order_total from items for reconciliation
    # - Use inner merge so orders without items are dropped (avoids NaN totals)
    # - Ensure float dtype for order_total
    # ---------------------------
    item_sums = (
        order_items.assign(line_amount=lambda d: d["qty"] * d["unit_price"])
        .groupby("order_id", as_index=False)["line_amount"]
        .sum()
        .rename(columns={"line_amount": "order_total"})
    )

    # Drop any stale raw totals and recompute strictly from items
    orders = (
        orders.drop(columns=["order_total"], errors="ignore")
              .merge(item_sums, on="order_id", how="inner")
    )

    # Remove orders missing timestamp after parsing
    orders = orders.dropna(subset=["order_ts"])

    # Column order: exact contract expected by validate.py
    orders = orders[["order_id", "customer_id", "order_ts", "status", "currency", "order_total"]]
    order_items = order_items[["order_id", "product_id", "qty", "unit_price"]]

    # ---------------------------
    # Writes
    # ---------------------------
    write_parquet(orders, SILVER / "stg_orders.parquet")
    write_parquet(order_items, SILVER / "stg_order_items.parquet")
