# Auto Loader Hands-On

## Overview

This hands-on notebook demonstrates **incremental data ingestion from files** using **Databricks Auto Loader** with a **bookstore dataset** containing three Delta tables: **Customers**, **Orders**, and **Books**.
The example shows how to:

* Configure Auto Loader to read Parquet files.
* Continuously ingest new files from a source directory.
* Persist data to a Delta table with exactly-once guarantees.
* Monitor ingestion progress and table updates.

---

## Dataset Setup

* The dataset is prepared using a provided **copy dataset script**.
* Data source: A directory containing Parquet files representing new orders.
* Initially, the directory contains **one Parquet file**.

---

## Auto Loader Configuration

### Streaming Read

Auto Loader uses **Spark Structured Streaming** APIs:

```python
df = spark.readStream \
    .format("cloudFiles") \
    .option("cloudFiles.format", "parquet") \
    .option("cloudFiles.schemaLocation", "/path/to/schema_and_checkpoint") \
    .load("/path/to/source")
```

**Parameters**:

* **`cloudFiles.format`**: Specifies file format (e.g., Parquet, CSV, JSON).
* **`cloudFiles.schemaLocation`**: Stores inferred schema for reuse, avoiding schema inference cost on every restart.
* **`load()`**: Points to the directory where new files will appear.

---

### Streaming Write

The streaming DataFrame is written directly to a Delta table:

```python
df.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/path/to/schema_and_checkpoint") \
    .toTable("orders_updates")
```

**Notes**:

* Same directory is used for **schema storage** and **checkpointing**.
* Checkpointing ensures:

  * Exactly-once ingestion.
  * Resume capability after failures.
  * Tracking of ingested files.

---

## Continuous Ingestion Process

* Auto Loader runs as a **streaming query**, continuously detecting and ingesting new files.
* Ingested data is written to a Delta table (`orders_updates`).
* Once loaded, the data is queryable like any static Delta table.

**Initial Check**:

```sql
SELECT COUNT(*) FROM orders_updates;
```

Example result: `1000` records (from initial file).

---

## Simulating New Data Arrival

The demo simulates new files arriving via a helper function:

* Each execution adds a new Parquet file (1,000 records) to the source directory.
* Example:

  * First run: `+1000` records.
  * Second run: `+1000` more records.
* The directory listing confirms the presence of new files.

---

## Auto Loader Detection and Processing

* Auto Loader **automatically detects new files** and queues them for ingestion.
* The **Databricks streaming dashboard** shows:

  * Active query status.
  * Batch progress.
  * New data ingestion rate.

**Post-ingestion check**:

```sql
SELECT COUNT(*) FROM orders_updates;
```

Example result: `3000` records after two additional files were processed.

---

## Table History and Versioning

Delta Lake **table history** confirms:

* A new version is created for each batch processed.
* Update events correspond to batches of new files detected by Auto Loader.

```sql
DESCRIBE HISTORY orders_updates;
```

---

## Cleanup

To stop ingestion and reset the environment:

```sql
DROP TABLE orders_updates;
```

Remove checkpoint/schema storage directory:

```bash
dbutils.fs.rm("/path/to/schema_and_checkpoint", recurse=True)
```

---

## Key Points

* **Auto Loader**:

  * Scalable, incremental file ingestion.
  * Exactly-once guarantees through checkpointing.
  * Automatic schema detection and evolution.
* **Best Practices**:

  * Store `cloudFiles.schemaLocation` and `checkpointLocation` in a reliable, persistent path.
  * Monitor ingestion via the Databricks streaming dashboard.
  * Clean up active streams and checkpoint data when finished.
