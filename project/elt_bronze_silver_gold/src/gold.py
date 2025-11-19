import pandas as pd

from .config import SILVER, GOLD
from .io_utils import reset_dir, write_parquet, write_csv, now_utc_iso

def gold_build() -> None:
    reset_dir(GOLD)

    customers = pd.read_parquet(SILVER / "dim_customer.parquet")
    products = pd.read_parquet(SILVER / "dim_product.parquet")
    orders = pd.read_parquet(SILVER / "stg_orders.parquet")
    order_items = pd.read_parquet(SILVER / "stg_order_items.parquet")

    fact_line = (
        order_items
        .merge(orders[["order_id", "customer_id", "order_ts", "status", "currency"]], on="order_id", how="inner")
        .merge(products[["product_id", "sku", "category"]], on="product_id", how="left")
        .merge(customers[["customer_id", "country"]], on="customer_id", how="left")
    )
    fact_line["extended_amount"] = fact_line["qty"] * fact_line["unit_price"]
    write_parquet(fact_line, GOLD / "fact_order_line.parquet")

    # tz-naive before to_period to avoid warnings
    dim_date = pd.DataFrame({
        "date": pd.to_datetime(pd.Series(pd.to_datetime(orders["order_ts"]).dt.date.unique()))
    })
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["day"] = dim_date["date"].dt.day
    dim_date["ym"] = dim_date["date"].dt.to_period("M").astype(str)
    write_parquet(dim_date, GOLD / "dim_date.parquet")

    agg_monthly = (
        fact_line
        .assign(ym=lambda df: pd.to_datetime(df["order_ts"]).dt.tz_localize(None).dt.to_period("M").astype(str))
        .groupby(["ym", "country", "currency"], as_index=False)
        .agg(
            orders=("order_id", "nunique"),
            items=("order_id", "size"),
            revenue=("extended_amount", "sum"),
        )
        .sort_values(["ym", "country", "currency"])
    )
    write_parquet(agg_monthly, GOLD / "agg_monthly_revenue.parquet")
    write_csv(agg_monthly, GOLD / "agg_monthly_revenue.csv")

    active_products = products.query("active == True")["product_id"].nunique()

    orders_paid = orders.query("status in ['paid','shipped']")
    paid_ids = set(orders_paid["order_id"].tolist())

    fact_paid = fact_line[fact_line["order_id"].isin(paid_ids)]
    order_sums = (
        fact_paid.groupby("order_id", as_index=False)
        .agg(order_amount=("extended_amount", "sum"))
    )

    if order_sums.empty:
        arpo_val = None
    else:
        arpo_val = float(order_sums["order_amount"].mean())

    kpi = pd.DataFrame({
        "extracted_at": [now_utc_iso()],
        "active_products": [int(active_products)],
        "arpo_paid_orders": [round(arpo_val, 2) if arpo_val is not None else None],
    })
    write_csv(kpi, GOLD / "kpi_snapshot.csv")
