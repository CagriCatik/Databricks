# Structured Streaming

## Overview

Structured Streaming in Databricks is a scalable and fault-tolerant stream processing engine built on Apache Spark. It allows developers to process continuously arriving data in near real-time by treating the data stream as an unbounded table. New data is handled as appended rows, enabling incremental processing with strong processing guarantees.

---

## Key Concepts

### Data Stream

A **data stream** is any data source that grows over time, including:

* New JSON log files landing in cloud storage
* Change Data Capture (CDC) feeds from databases
* Events in a publish/subscribe messaging system like Kafka

---

## Traditional vs Streaming Processing

**Traditional Approach**:

* Reprocesses the entire dataset on each update

**Incremental Approach**:

* Captures and processes only the newly arrived data since the last execution
* Spark Structured Streaming implements this incremental approach efficiently

---

## Spark Structured Streaming Architecture

* Queries **infinite data sources**
* Automatically detects new data
* Persists results incrementally to a **sink** (e.g., file storage, tables)
* Treats the source as an **unbounded table** for query purposes

---

## Sources and Integration

Structured Streaming supports various sources:

* File directories
* Messaging systems (Kafka, etc.)
* Delta Lake tables

**Delta Lake Integration**:

* Use `spark.readStream()` to read Delta tables as streaming sources
* Processes existing and new data seamlessly
* Outputs are managed using `DataFrame.writeStream()`

---

## Streaming Query Workflow

1. **Read** from a streaming source:

   ```python
   df = spark.readStream.format("delta").load("/path/to/table")
   ```
2. **Transform** data as with static DataFrames
3. **Write** results to a sink:

   ```python
   df.writeStream.format("delta") \
       .outputMode("append") \
       .trigger(processingTime="2 minutes") \
       .option("checkpointLocation", "/path/to/checkpoint") \
       .start("/path/to/output")
   ```

---

## Trigger Configuration

**Trigger** specifies when to process new data:

* Default: every 0.5 seconds
* Fixed interval: e.g., `processingTime="5 minutes"`
* Batch mode:

  * **`trigger(once=True)`**: process all available data in one batch
  * **`trigger(availableNow=True)`**: process available data in multiple micro-batches until completion

---

## Output Modes

* **Append (default)**: Only new rows are appended to the sink
* **Complete**: Entire result table is recalculated and written each trigger

---

## Checkpointing and Fault Tolerance

**Checkpointing**:

* Stores the streaming query state in cloud storage
* Required for exactly-once processing
* Each stream must have a **unique** checkpoint location

**Write-Ahead Logs (WAL)**:

* Tracks the offset range for each trigger
* Enables recovery from failures without data duplication

---

## Processing Guarantees

* **Exactly-once** semantics
* Idempotent sinks prevent duplicate data writes
* Guarantees depend on:

  * Repeatable sources (e.g., object storage, Kafka)
  * Idempotent sinks (e.g., Delta Lake)

---

## Limitations

Not all operations are supported on streaming DataFrames:

* Full sorting
* Certain deduplication scenarios

Advanced techniques like **windowing** and **watermarking** can be used to enable such operations where logically possible.

---

## Example: Delta Streaming with Trigger

```python
# Read from Delta as a streaming source
df = spark.readStream.format("delta").load("/delta/events")

# Apply transformations
processed_df = df.filter(df.value > 100)

# Write to Delta sink with checkpointing and 2-minute trigger
processed_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .trigger(processingTime="2 minutes") \
    .option("checkpointLocation", "/checkpoints/events") \
    .start("/delta/processed_events")
```

---

## Summary

* Treats continuous data as an unbounded table
* Supports micro-batch and continuous processing
* Integrates with Delta Lake for seamless real-time processing
* Provides strong fault tolerance via checkpointing and WAL
* Guarantees exactly-once semantics with repeatable sources and idempotent sinks
* Some operations require specialized streaming techniques
