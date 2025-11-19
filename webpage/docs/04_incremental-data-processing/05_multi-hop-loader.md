# Databricks Multi-Hop Loader (Medallion Architecture) Documentation

## Overview

The **Multi-Hop Architecture**, also known as the **Medallion Architecture**, is a data design pattern in the **Lakehouse** that organizes data in multiple logical layers — **Bronze**, **Silver**, and **Gold** — to incrementally improve **data quality** and **structure** as it flows through the pipeline.
It supports both **batch** and **streaming** processing, enabling scalable, maintainable, and recoverable ETL workflows.

---

## Incremental Multi-Hop Pipeline

An **incremental multi-hop pipeline** processes data in stages, where each stage:

* Consumes the output of the previous stage.
* Applies transformations to improve the data quality.
* Writes to a new table representing a higher-level, refined dataset.

---

## Architecture Layers

### 1. Bronze Layer

**Purpose**: Store **raw ingested data** exactly as received, without transformations.

**Characteristics**:

* Data sources: JSON files, operational databases, Kafka streams, etc.
* Minimal processing — ingestion only.
* Preserves original data for **replay** and **reprocessing**.
* Schema often directly reflects the source.

**Example**:

```python
bronze_df = spark.readStream.format("cloudFiles") \
    .option("cloudFiles.format", "json") \
    .load("/data/raw/orders")

bronze_df.writeStream.format("delta") \
    .option("checkpointLocation", "/checkpoints/bronze") \
    .toTable("orders_bronze")
```

---

### 2. Silver Layer

**Purpose**: Provide a **cleaned and enriched view** of the data.

**Transformations**:

* Data cleansing (remove duplicates, handle nulls).
* Filtering.
* Joining with other datasets to enrich records.
* Normalizing field names and formats.

**Example**:

```python
silver_df = spark.table("orders_bronze") \
    .filter("status IS NOT NULL") \
    .join(spark.table("customers_bronze"), "customer_id")

silver_df.writeStream.format("delta") \
    .option("checkpointLocation", "/checkpoints/silver") \
    .toTable("orders_silver")
```

---

### 3. Gold Layer

**Purpose**: Deliver **business-level aggregates** and analytics-ready datasets.

**Use Cases**:

* Reporting and dashboarding.
* Machine learning model training.
* KPI computation.

**Example**:

```python
gold_df = spark.table("orders_silver") \
    .groupBy("region") \
    .agg({"amount": "sum"})

gold_df.writeStream.format("delta") \
    .option("checkpointLocation", "/checkpoints/gold") \
    .toTable("orders_gold")
```

---

## Benefits of Multi-Hop Architecture

* **Simplicity**: Clear separation of responsibilities across layers.
* **Incremental ETL**: Only process new data at each stage.
* **Flexibility**: Mix batch and streaming jobs in the same pipeline.
* **Recoverability**: Recreate refined tables from raw data at any time.
* **Data Quality Improvement**: Quality and structure improve at each hop.
* **Reusability**: Bronze and silver layers can serve multiple downstream applications.

---

## Processing Modes

Each layer can be configured as:

* **Batch**: For periodic processing.
* **Streaming**: For real-time or near-real-time ingestion and transformation.

---

## Best Practices

* Keep **bronze tables immutable** to preserve a reliable raw data record.
* Apply **idempotent transformations** in silver and gold to ensure consistency.
* Store **checkpoints** for all streaming jobs to enable recovery.
* Use **partitioning** in gold tables to optimize query performance.
* Leverage **Delta Lake time travel** for auditing and debugging.
