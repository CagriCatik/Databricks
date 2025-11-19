# Delta Lake

- Delta Lake is an open-source storage framework that brings **ACID transactions**, **scalable metadata handling**, and **unified batch and streaming data processing** to data lakes. 
- It acts as a **storage layer**—not a format, storage medium, database, or warehouse—providing **reliability** to data lakes and enabling the **Lakehouse architecture**.

---

## Overview

Delta Lake sits on top of existing cloud storage systems (e.g., AWS S3, Azure Data Lake, GCS) and enhances traditional data lakes with:

- ACID transactions
- Scalable metadata management
- Schema enforcement and evolution
- Time travel
- Unified batch and streaming

It integrates directly into the **Databricks Runtime** and is also supported by open-source Spark deployments.

---

## Delta Lake vs Traditional Data Lakes

| Feature                        | Traditional Data Lakes | Delta Lake           |
|-------------------------------|------------------------|----------------------|
| ACID Transactions             | No                     | Yes                  |
| Schema Enforcement            | No                     | Yes                  |
| Metadata Scalability          | Limited (file listing) | High (transaction log) |
| Time Travel                   | No                     | Yes                  |
| Streaming + Batch Unification | No                     | Yes                  |

---

## Core Components

### Data Files

Delta Lake stores actual table content as **Parquet files**.

### Transaction Log (`_delta_log`)

Every table directory contains a `_delta_log` folder:

- Contains JSON files recording all operations (writes, updates, deletes)
- Serves as the **single source of truth**
- Enables reconstructing the exact state of a table at any point in time

---

## Delta Log Mechanics

### Scenario 1: Initial Write

1. **Writer** writes data to two Parquet files: `file1.parquet`, `file2.parquet`
2. Writer appends `000000.json` to `_delta_log`, recording metadata for both files.
3. **Reader** consults `000000.json` and reads files 1 and 2.

### Scenario 2: Update Operation

1. **Writer** modifies a record in `file1.parquet`.
2. Delta Lake **does not update in place**. Instead:
   - Creates `file3.parquet` with the updated content.
   - Marks `file1.parquet` as removed.
3. A new log file `000001.json` records:
   - The updated file
   - The removal of the old file
4. **Reader** reads `file2.parquet` and `file3.parquet` only.

### Scenario 3: Concurrent Read/Write

- **Writer** starts writing `file4.parquet` but has not yet committed.
- **Reader** consults current transaction log (e.g., `000001.json`), which does not mention `file4.parquet`.
- Reader proceeds safely with existing committed files (`file2`, `file3`).

### Scenario 4: Failed Write

- **Writer** attempts to write `file5.parquet` but the job fails.
- No new log file is committed.
- **Reader** reads the latest log, which **excludes** the incomplete `file5.parquet`.

---

## Key Guarantees

- **ACID compliance**: All changes are atomic, consistent, isolated, and durable.
- **No dirty reads**: Incomplete or failed writes are never exposed.
- **Serializability**: Concurrent operations do not conflict.
- **Time travel**: Snapshot-based querying using transaction history.
- **Full audit trail**: Every change is logged and queryable.

---

## Supported File Formats

| Type         | Format Used   |
|--------------|----------------|
| Data files   | Parquet        |
| Log records  | JSON           |

Delta Lake uses open-source, columnar, and structured formats to maintain compatibility and performance.

---

## Next Step

Proceed to Databricks notebooks to explore Delta Lake functionality with practical examples.
