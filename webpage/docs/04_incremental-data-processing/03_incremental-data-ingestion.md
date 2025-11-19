# Incremental Data Ingestion

## Overview

Incremental data ingestion in Databricks is the process of loading only **new files** that have appeared in a storage location since the last ingestion run, avoiding reprocessing of previously loaded files.
Databricks provides two primary mechanisms for incremental file ingestion:

1. **COPY INTO** SQL command
2. **Auto Loader** (based on Spark Structured Streaming)

---

## Goals of Incremental Ingestion

* Process only **newly arrived data files**.
* Avoid redundant processing of files already ingested.
* Support scalability from thousands to millions of files.
* Provide **idempotency** (safe to re-run without duplication).

---

## Method 1: COPY INTO Command

### Description

The `COPY INTO` command is a SQL-based ingestion method for loading data from a file location into a **Delta table**.
It supports **incremental** and **idempotent** ingestion.

### How It Works

* Loads only files **not previously loaded** into the target table.
* Skips files already processed.
* Supports multiple file formats (CSV, Parquet, etc.).
* Allows schema evolution during ingestion.

### Syntax Example

```sql
COPY INTO delta_table
FROM 's3://bucket/path/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'delimiter' = '|')
COPY_OPTIONS ('mergeSchema' = 'true');
```

**Key Features**:

* **`FILEFORMAT`**: Specifies source file format.
* **`FORMAT_OPTIONS`**: Defines format-specific parameters.
* **`COPY_OPTIONS`**: Controls operational behavior (e.g., schema evolution with `mergeSchema`).

### When to Use

* File volumes in **thousands**.
* Ingestion runs that can be executed manually or scheduled at intervals.
* Simple SQL-based ingestion requirements.

---

## Method 2: Auto Loader

### Description

**Auto Loader** uses **Spark Structured Streaming** to continuously and efficiently ingest new files from cloud storage. It is designed for **high-scale, near-real-time ingestion**.

### How It Works

* Uses a **streaming read** via `spark.readStream`.
* Specialized source format: `"cloudFiles"`.
* Detects new files and queues them for ingestion.
* Uses **checkpointing** to store ingestion progress and file metadata.
* Guarantees **exactly-once** processing.
* Automatically detects schema changes and can store inferred schema for reuse.

### PySpark Example

```python
df = spark.readStream \
    .format("cloudFiles") \
    .option("cloudFiles.format", "parquet") \
    .option("cloudFiles.schemaLocation", "/path/to/schema") \
    .load("/path/to/source")

df.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/path/to/checkpoint") \
    .start("/path/to/target")
```

**Key Options**:

* **`cloudFiles.format`**: Source file format (CSV, Parquet, JSON, etc.).
* **`cloudFiles.schemaLocation`**: Directory where inferred schema is stored to avoid re-inferring on each startup.
* **`checkpointLocation`**: Tracks streaming state for exactly-once semantics.

### When to Use

* File volumes in **millions or more**.
* Continuous or near-real-time ingestion requirements.
* Scalable ingestion for cloud object storage (e.g., AWS S3, Azure Blob, GCS).
* Recommended **best practice** by Databricks for large-scale ingestion.

---

## Comparison: COPY INTO vs Auto Loader

| Feature / Criteria   | COPY INTO                       | Auto Loader                         |
| -------------------- | ------------------------------- | ----------------------------------- |
| **Execution Type**   | Batch (SQL command)             | Streaming (Structured Streaming)    |
| **Scalability**      | Thousands of files              | Millions+ of files                  |
| **Performance**      | Manual run per execution        | Continuous ingestion, micro-batches |
| **Fault Tolerance**  | Skips already processed files   | Checkpointing + resume on failure   |
| **Schema Evolution** | `mergeSchema` option            | Auto-detect with schema storage     |
| **Use Case**         | Small to medium ingestion needs | Large-scale, real-time ingestion    |
| **Idempotency**      | Yes                             | Yes                                 |

---

## Best Practices

* **COPY INTO**:

  * Use for small to medium datasets.
  * Ideal when ingestion is triggered periodically.
* **Auto Loader**:

  * Default choice for ingestion from cloud storage.
  * Store schema in `cloudFiles.schemaLocation` to reduce startup costs.
  * Ensure checkpointing is configured for exactly-once guarantees.
  * Consider partitioning target tables for optimized query performance.
