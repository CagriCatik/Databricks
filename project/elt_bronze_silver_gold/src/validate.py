# validate.py

import json
from hashlib import md5
import pandas as pd

from .config import BRONZE, SILVER, GOLD


def _failures_header(title: str):
    print(f"\n[Validate] {title}")


def _assert_true(cond: bool, msg: str, failures: list):
    if not cond:
        failures.append(msg)
        print(f"  FAIL: {msg}")
    else:
        print(f"  OK  : {msg}")


def _hash_df(df: pd.DataFrame) -> str:
    b = pd.util.hash_pandas_object(df, index=True).values
    return md5(b.tobytes() + ",".join(df.columns).encode()).hexdigest()


def validate() -> int:
    failures = []

    # -------- Artifacts exist --------
    required_paths = [
        SILVER / "dim_customer.parquet",
        SILVER / "dim_product.parquet",
        SILVER / "stg_orders.parquet",
        SILVER / "stg_order_items.parquet",
        GOLD / "fact_order_line.parquet",
        GOLD / "agg_monthly_revenue.parquet",
        GOLD / "kpi_snapshot.csv",
    ]
    _failures_header("Artifacts exist")
    for p in required_paths:
        _assert_true(p.exists(), f"Found artifact: {p}", failures)

    if failures:
        return _exit_validation(failures)

    # -------- Load data --------
    dim_customer = pd.read_parquet(SILVER / "dim_customer.parquet")
    dim_product = pd.read_parquet(SILVER / "dim_product.parquet")
    stg_orders = pd.read_parquet(SILVER / "stg_orders.parquet")
    stg_items = pd.read_parquet(SILVER / "stg_order_items.parquet")
    fact_line = pd.read_parquet(GOLD / "fact_order_line.parquet")
    agg_monthly = pd.read_parquet(GOLD / "agg_monthly_revenue.parquet")

    # -------- Schema contracts --------
    _failures_header("Schema contracts")
    expected_dim_customer_cols = ["customer_id", "email", "country", "signup_ts"]
    expected_dim_product_cols = ["product_id", "sku", "name", "category", "unit_price", "active"]
    expected_stg_orders_cols = ["order_id", "customer_id", "order_ts", "status", "currency", "order_total"]
    expected_stg_items_cols = ["order_id", "product_id", "qty", "unit_price"]

    _assert_true(list(dim_customer.columns) == expected_dim_customer_cols, "dim_customer columns exact match", failures)
    _assert_true(list(dim_product.columns) == expected_dim_product_cols, "dim_product columns exact match", failures)
    _assert_true(list(stg_orders.columns) == expected_stg_orders_cols, "stg_orders columns exact match", failures)
    _assert_true(list(stg_items.columns) == expected_stg_items_cols, "stg_order_items columns exact match", failures)

    _assert_true(pd.api.types.is_integer_dtype(dim_customer["customer_id"]), "dim_customer.customer_id dtype is integer", failures)
    _assert_true(pd.api.types.is_integer_dtype(dim_product["product_id"]), "dim_product.product_id dtype is integer", failures)
    _assert_true(pd.api.types.is_integer_dtype(stg_orders["order_id"]), "stg_orders.order_id dtype is integer", failures)
    _assert_true(pd.api.types.is_datetime64_any_dtype(dim_customer["signup_ts"]), "dim_customer.signup_ts is datetime", failures)
    _assert_true(pd.api.types.is_datetime64_any_dtype(stg_orders["order_ts"]), "stg_orders.order_ts is datetime", failures)

    # -------- Nulls and uniqueness --------
    _failures_header("Nulls and uniqueness")
    _assert_true(dim_customer["customer_id"].notna().all(), "PK not null: dim_customer.customer_id", failures)
    _assert_true(dim_customer["customer_id"].is_unique, "PK unique: dim_customer.customer_id", failures)
    _assert_true(dim_product["product_id"].notna().all(), "PK not null: dim_product.product_id", failures)
    _assert_true(dim_product["product_id"].is_unique, "PK unique: dim_product.product_id", failures)
    _assert_true(stg_orders["order_id"].notna().all(), "PK not null: stg_orders.order_id", failures)
    _assert_true(stg_orders["order_id"].is_unique, "PK unique: stg_orders.order_id", failures)
    _assert_true(stg_items[["order_id", "product_id"]].notna().all().all(), "FK columns not null: stg_order_items.(order_id, product_id)", failures)
    _assert_true((stg_items["qty"] > 0).all(), "qty > 0 in stg_order_items", failures)
    _assert_true((stg_items["unit_price"] >= 0).all(), "unit_price >= 0 in stg_order_items", failures)

    # -------- Domain checks --------
    _failures_header("Domain checks")
    allowed_status = {"created", "paid", "shipped", "cancelled"}
    allowed_currency = {"EUR", "USD", "TRY"}
    _assert_true(set(stg_orders["status"].unique()).issubset(allowed_status), "status domain ok", failures)
    _assert_true(set(stg_orders["currency"].unique()).issubset(allowed_currency), "currency domain ok", failures)
    _assert_true(stg_orders["order_total"].notna().all(), "order_total not null", failures)

    # -------- Referential integrity --------
    _failures_header("Referential integrity")
    missing_cust = stg_orders.merge(dim_customer[["customer_id"]], on="customer_id", how="left", indicator=True)
    _assert_true((missing_cust["_merge"] != "left_only").all(), "orders.customer_id present in dim_customer", failures)

    missing_prod = stg_items.merge(dim_product[["product_id"]], on="product_id", how="left", indicator=True)
    _assert_true((missing_prod["_merge"] != "left_only").all(), "order_items.product_id present in dim_product", failures)

    # QA reports are informational (non-fatal)
    qa_bad_orders = SILVER / "qa_bad_orders_missing_customer.parquet"
    qa_bad_items = SILVER / "qa_bad_items_missing_product.parquet"
    if qa_bad_orders.exists():
        print(f"  OK  : QA bad orders count: {len(pd.read_parquet(qa_bad_orders))}")
    if qa_bad_items.exists():
        print(f"  OK  : QA bad items count: {len(pd.read_parquet(qa_bad_items))}")

    # -------- Reconciliations --------
    _failures_header("Reconciliations")

    # Per-order reconciliation
    tol = 1.0
    items_sum = (
        stg_items.assign(line_amount=lambda d: d["qty"] * d["unit_price"])
        .groupby("order_id", as_index=False)["line_amount"]
        .sum()
    )
    ords = stg_orders.merge(items_sum, on="order_id", how="left")
    ords["diff"] = (ords["line_amount"].fillna(0.0) - ords["order_total"].fillna(0.0)).abs()
    bad_recon = ords[ords["diff"] > tol]
    _assert_true(bad_recon.empty, f"order_items sums reconcile to stg_orders.order_total within {tol}", failures)

    # Gold vs fact_line grouped
    fact_line_chk = (
        fact_line.assign(ym=lambda d: pd.to_datetime(d["order_ts"]).dt.tz_localize(None).dt.to_period("M").astype(str))
        .groupby(["ym", "country", "currency"], as_index=False)
        .agg(
            rev=("extended_amount", "sum"),
            orders=("order_id", "nunique"),
            items=("order_id", "size"),
        )
    )
    merged = agg_monthly.merge(
        fact_line_chk, on=["ym", "country", "currency"], how="outer", suffixes=("_gold", "_calc")
    ).fillna(0.0)

    merged["rev_diff"] = (merged["revenue"] - merged["rev"]).abs()
    _assert_true((merged["rev_diff"] <= 1e-6).all(), "Gold revenue equals grouped fact_line revenue", failures)
    _assert_true((merged["orders_gold"] == merged["orders_calc"]).all(), "Gold orders count equals grouped fact_line", failures)
    _assert_true((merged["items_gold"] == merged["items_calc"]).all(), "Gold items count equals grouped fact_line", failures)

    # -------- Business rules --------
    _failures_header("Business rules")
    paid_shipped_ids = set(stg_orders.query("status in ['paid','shipped']")["order_id"].tolist())
    kpi_df = pd.read_csv(GOLD / "kpi_snapshot.csv")
    fact_paid = fact_line[fact_line["order_id"].isin(paid_shipped_ids)]
    arpo_calc = (
        fact_paid.groupby("order_id", as_index=False)
        .agg(order_amount=("extended_amount", "sum"))["order_amount"]
        .mean()
    )
    arpo_calc_round = None if pd.isna(arpo_calc) else round(float(arpo_calc), 2)
    _assert_true(
        (kpi_df["arpo_paid_orders"].iloc[0] == arpo_calc_round),
        "KPI ARPO matches recomputed paid/shipped ARPO",
        failures,
    )

    # -------- Freshness --------
    _failures_header("Freshness")
    meta_path = BRONZE / "_landing_metadata.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        _assert_true("landed_at" in meta, "landing metadata has landed_at", failures)

    return _exit_validation(failures)


def _exit_validation(failures: list) -> int:
    if failures:
        print(f"\n[Validate] FAILED with {len(failures)} error(s).")
        for i, msg in enumerate(failures, 1):
            print(f"  {i}. {msg}")
        return 1
    else:
        print("\n[Validate] PASSED.")
        return 0
