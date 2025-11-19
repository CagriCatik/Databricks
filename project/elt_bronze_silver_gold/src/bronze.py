import json
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd

from .config import BRONZE
from .io_utils import reset_dir, write_csv, now_utc_iso

def generate_raw() -> None:
    reset_dir(BRONZE)

    rng = np.random.default_rng(42)
    n_customers = 20
    customers = pd.DataFrame({
        "customer_id": np.arange(1, n_customers + 1),
        "email": [f"user{i}@example.com" for i in range(1, n_customers + 1)],
        "country": rng.choice(["DE", "US", "TR", "GB", "FR", None], size=n_customers,
                              p=[0.25, 0.25, 0.2, 0.15, 0.1, 0.05]),
        "signup_ts": [
            datetime(2025, 1, 1).strftime("%Y-%m-%d %H:%M:%S"),
            datetime(2025, 1, 2).strftime("%Y/%m/%d %H:%M:%S"),
        ] * (n_customers // 2) + [datetime(2025, 2, 1).strftime("%d-%m-%Y %H:%M:%S")] * (n_customers - (n_customers // 2) * 2),
    })
    customers = pd.concat([customers, customers.iloc[[0]]], ignore_index=True)
    write_csv(customers, BRONZE / "customers.csv")

    products = []
    for pid in range(1001, 1006):
        products.append({
            "product_id": int(pid),
            "sku": f"SKU-{pid}",
            "name": f"Widget {pid}",
            "category": str(np.random.choice(["A", "B", "C", "D"])),
            "unit_price": float(np.random.choice([9.99, 14.5, 20.0, 50.0])),
            "active": bool(np.random.choice([True, True, True, False]))
        })
    (BRONZE / "products.jsonl").write_text("\n".join(json.dumps(x) for x in products))

    n_orders = 100
    order_dates = pd.date_range("2025-03-01", periods=30, freq="D")
    orders = pd.DataFrame({
        "order_id": np.arange(5001, 5001 + n_orders),
        "customer_id": np.random.choice(customers["customer_id"].unique(), size=n_orders),
        "order_ts": np.random.choice(order_dates, size=n_orders).astype(str),
        "status": np.random.choice(["created", "paid", "shipped", "cancelled"], size=n_orders,
                                   p=[0.1, 0.6, 0.25, 0.05]),
        "currency": np.random.choice(["EUR", "USD", "TRY"], size=n_orders, p=[0.6, 0.3, 0.1]),
        "order_total": np.random.choice(["19.99", "49,99", "100.00", "14,50"], size=n_orders),
    })
    orders.loc[orders.sample(3, random_state=1).index, "customer_id"] = 99999
    write_csv(orders, BRONZE / "orders.csv")

    rows = []
    for oid in orders["order_id"]:
        k = np.random.choice([1, 2, 3], p=[0.5, 0.35, 0.15])
        chosen_products = np.random.choice(range(1001, 1006), size=k, replace=True)
        for pid in chosen_products:
            rows.append({
                "order_id": int(oid),
                "product_id": int(pid),
                "qty": int(np.random.choice([1, 1, 2, 3])),
                "unit_price": np.random.choice(["9.99", "14,50", "20.00", "50.00"]),
            })
    order_items = pd.DataFrame(rows)
    write_csv(order_items, BRONZE / "order_items.csv")

    (BRONZE / "_landing_metadata.json").write_text(json.dumps({
        "landed_at": now_utc_iso(),
        "source_systems": ["ecommerce-db", "catalog-service"],
        "note": "Demo bronze landing for ELT walkthrough."
    }, indent=2))
