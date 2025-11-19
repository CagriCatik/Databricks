# Databricks Structured Streaming Hands-On Documentation

## Overview

This hands-on example demonstrates how to use **Spark Structured Streaming** in Databricks to perform incremental data processing on a Delta Lake dataset. The exercise builds upon a bookstore dataset with three tables: **Customers**, **Orders**, and **Books**, showing how to:

* Read data as a streaming source
* Use streaming temporary views in SQL
* Persist streaming results to durable storage
* Configure trigger modes and output settings
* Monitor and control streaming queries

---

## Dataset Preparation

Before streaming operations begin, the bookstore dataset is copied to the working environment.

---

## Reading a Streaming Source

### PySpark `readStream`

Streaming queries require the **PySpark API**:

```python
spark.readStream.format("delta").load("/path/to/source")
```

* Reads a **Delta table** as a streaming source.
* Produces a **streaming DataFrame**.

### Registering a Streaming Temporary View

```python
df.createOrReplaceTempView("books_streaming")
```

* Registers a **streaming temporary view** for SQL queries.
* SQL transformations on this view are applied as **streaming queries**.
* Output is continuously updated until the query is manually stopped.

---

## Interactive Exploration

### Streaming Query Behavior

* Streaming SQL queries run **indefinitely** until canceled.
* They are suitable for **live monitoring** or **dashboarding**.
* Active queries consume resources and should be canceled when not in use.

Example cancellation:

```python
spark.streams.active[0].stop()
```

---

## Aggregations in Streaming

* SQL aggregations on streaming temporary views result in streaming aggregations.
* These queries:

  * Run continuously
  * Do **not** persist results unless explicitly written
* Not all operations are supported (e.g., sorting).
  For complex use cases, **windowing** and **watermarking** are required.

---

## Persisting Streaming Results

### Converting Back to DataFrame API

To persist, logic must be returned to the **PySpark DataFrame API**:

```python
df_stream = spark.table("books_streaming")
```

* A streaming view always produces a **streaming DataFrame**.
* Incremental processing must be defined from the beginning with a streaming read.

### Writing with `writeStream`

```python
df_stream.writeStream \
    .format("delta") \
    .outputMode("complete") \
    .trigger(processingTime="4 seconds") \
    .option("checkpointLocation", "/path/to/checkpoints") \
    .start("/path/to/target")
```

**Configuration parameters**:

* **Trigger Interval**: `processingTime="4 seconds"` — processes every 4 seconds.
* **Output Mode**:

  * `append`: Only new records are added.
  * `complete`: Required for aggregations; overwrites with each trigger.
* **Checkpoint Location**: Tracks query state for recovery and exactly-once semantics.

---

## Monitoring Streaming Queries

* Databricks provides an **interactive dashboard** for streaming queries.
* Displays:

  * Processing rates
  * Input/output row counts
  * Trigger durations

---

## Updating the Source and Target

Streaming queries update target tables automatically when new data arrives at the source:

1. Add new records to the source table (e.g., **Books** table).
2. The active streaming query processes them and updates the target table.
3. Queries on the target table (non-streaming) show updated results.

---

## Best Practices

* Always **cancel active streams** when done:

  ```python
  for s in spark.streams.active:
      s.stop()
  ```
* Prevents unwanted resource consumption and avoids blocking cluster auto-termination.

---

## Changing Trigger Modes

### Always-On Micro-Batch

* Trigger every fixed interval (e.g., every 4 seconds).
* Runs continuously until manually stopped.

### Batch Mode with `availableNow`

```python
df_stream.writeStream \
    .trigger(availableNow=True) \
    .start("/path/to/target") \
    .awaitTermination()
```

* Processes **all available new data** and stops automatically.
* `awaitTermination()` blocks execution until processing completes.

---

## Example Workflow

1. **Read streaming source**:

   ```python
   df = spark.readStream.format("delta").load("/delta/books")
   df.createOrReplaceTempView("books_streaming")
   ```

2. **Aggregation in SQL**:

   ```sql
   SELECT author, COUNT(*) AS book_count
   FROM books_streaming
   GROUP BY author
   ```

3. **Persist to target**:

   ```python
   spark.table("books_streaming") \
       .groupBy("author") \
       .count() \
       .writeStream \
       .format("delta") \
       .outputMode("complete") \
       .trigger(processingTime="4 seconds") \
       .option("checkpointLocation", "/checkpoints/authors") \
       .start("/delta/author_counts")
   ```

4. **Update source data** and verify target table reflects changes.

---

## Summary

* **Streaming temporary views** allow SQL queries on live data.
* Use `writeStream` for **incremental persistence**.
* Configure **trigger intervals**, **output modes**, and **checkpoints**.
* Switch between **always-on** and **availableNow** modes depending on requirements.
* Always cancel unused streams to release resources.
