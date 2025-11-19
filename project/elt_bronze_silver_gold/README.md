# ELT Bronze-Silver-Gold

This repository implements a self-contained ELT pipeline that lands synthetic raw data in **Bronze**, cleans and conforms it in **Silver**, and publishes analytics-ready marts in **Gold**. It also includes a validation step that fails fast if data quality expectations are violated.

* Bronze: raw, immutable files (CSV, JSONL)
* Silver: cleaned and typed tables (Parquet)
* Gold: fact tables, aggregates, and KPIs (Parquet + CSV)
* Validate: schema, integrity, reconciliation, and business-rule checks

---

## Requirements

* Python 3.10+ recommended
* Packages:

  * pandas
  * numpy
  * pyarrow (for Parquet I/O)

Install these via `requirements.txt` (below).

---

## Setup

* python -m venv venv
* venv\Scripts\activate
* pip install -r requirements.txt

`requirements.txt`:

```sh
pandas>=2.2
numpy>=1.26
pyarrow>=16.0
```

---

## Run

```sh
python -m src.cli bronze
python -m src.cli silver
python -m src.cli gold
python -m src.cli all
python -m src.cli validate
```

* `bronze`: generates synthetic raw data and lands it to disk.
* `silver`: parses timestamps and money, normalizes categories, de-duplicates, and writes typed Parquet tables. Produces QA reports for missing foreign keys.
* `gold`: builds a denormalized fact table, a date dimension, monthly revenue aggregates, and a KPI snapshot (active products and ARPO).
* `all`: runs `bronze -> silver -> gold` end-to-end.
* `validate`: asserts schema, nulls/uniqueness, referential integrity, reconciles totals, and checks business rules. Exits non-zero on failure.

---

## Project Layout

```sh
.
├─ data/
│  ├─ bronze/
│  ├─ silver/
│  └─ gold/
└─ src/
   ├─ __init__.py
   ├─ config.py        # Paths for data layers
   ├─ io_utils.py      # I/O helpers and timestamp utility
   ├─ bronze.py        # Synthetic raw data generator
   ├─ silver.py        # Cleaning, typing, conformance
   ├─ gold.py          # Fact, dims, aggregates, KPIs
   └─ cli.py           # CLI entrypoint and orchestration
```

> Note: The package is named `src`. If you use a different package name, adjust commands accordingly.

---

## Data Artifacts

After running `python -m src.cli all`, you should see:

**Bronze** (`data/bronze/`)

* `customers.csv`
* `orders.csv`
* `order_items.csv`
* `products.jsonl`
* `_landing_metadata.json`

**Silver** (`data/silver/`)

* `dim_customer.parquet`
* `dim_product.parquet`
* `stg_orders.parquet`
* `stg_order_items.parquet`
* `qa_bad_orders_missing_customer.parquet` (empty when all FKs present)
* `qa_bad_items_missing_product.parquet` (empty when all FKs present)

**Gold** (`data/gold/`)

* `fact_order_line.parquet`
* `dim_date.parquet`
* `agg_monthly_revenue.parquet`
* `agg_monthly_revenue.csv`
* `kpi_snapshot.csv` (columns: `extracted_at`, `active_products`, `arpo_paid_orders`)

---

## What the Pipeline Does

1. **Bronze**

   * Creates synthetic customers, orders, and order_items with mixed timestamp and currency formats.
   * Introduces a few referential issues deliberately; Silver flags these in QA outputs.

2. **Silver**

   * `parse_mixed_ts`: parses multiple timestamp formats into UTC.
   * `parse_money`: normalizes commas vs dots and converts to float.
   * De-duplicates customers, normalizes categories and email, enforces non-null critical fields.
   * Writes typed Parquet staging and dimension tables.
   * Emits QA Parquet reports for missing foreign keys.

3. **Gold**

   * Builds `fact_order_line` with `extended_amount = qty * unit_price`.
   * Derives a date dimension and a monthly grain (`ym`).
   * Aggregates monthly revenue by `(ym, country, currency)`.
   * Computes ARPO for paid/shipped orders and writes `kpi_snapshot.csv`.

4. **Validate**

   * Confirms expected columns and dtypes in Silver.
   * Enforces domain sets for `status` and `currency`.
   * Checks PK uniqueness, non-null constraints, and FK integrity.
   * Reconciles `order_total` vs item sums within a tolerance.
   * Verifies Gold monthly aggregates equal grouped `fact_order_line`.
   * Confirms KPI ARPO equals a recomputation from `fact_order_line`.

---

## Typical Commands

End-to-end run:

```sh
python -m src.cli all
```

Data quality validation:

```sh
python -m src.cli validate
```

Step-by-step:

```sh
python -m src.cli bronze
python -m src.cli silver
python -m src.cli gold
```

Cleanup of layer folders (manual):

* Delete `data/bronze`, `data/silver`, `data/gold`, then re-run.

---

## Exit Codes

* `0`: success
* Non-zero: validation failure or runtime error. Review console output for the failing assertion.

---

## Troubleshooting

1. `TypeError: Object of type bool is not JSON serializable`
   Cause: NumPy scalars in JSON.
   Status: Already handled by casting to native types in Bronze product generation.

2. `KeyError: 'ARPO'` in Gold
   Cause: Chained `.agg` misuse.
   Status: Fixed by computing ARPO in two steps and handling empty result sets.

3. `ImportError: Missing optional dependency 'pyarrow'`
   Cause: Parquet engine missing.
   Fix: `pip install pyarrow` or install via `requirements.txt`.

4. Timezone warnings when converting to monthly period
   Cause: Converting tz-aware timestamps directly to `Period`.
   Status: Code drops tz info before `to_period` in Gold to avoid warnings.

---

## Extending

* Replace local file I/O with S3/GCS/ADLS paths in `config.py`.
* Swap orchestration to Airflow or Prefect by calling the same module functions.
* Add more validations in `validate.py` as needed.
* Add more marts in `gold.py` (e.g., product or cohort analytics).

---

## Notes

* Synthetic data randomness: a fixed RNG seed is used for reproducibility in key places.
* Tolerance for reconciliations: set to `1.0` currency units. Adjust in `validate.py` if needed.
