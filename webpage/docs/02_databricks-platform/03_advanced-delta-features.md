# Advanced Delta Lake Features

- This guide outlines the advanced capabilities of Delta Lake including **time travel**, **file compaction**, **Z-Order indexing**, and **garbage collection** using the **VACUUM** command. 
- These features enable performant, maintainable, and recoverable data pipelines on data lake storage.

---

## Time Travel

Delta Lake automatically versions all changes to tables. This allows:

- Auditing historical changes
- Point-in-time queries
- Safe rollbacks

### View Table History

```sql
DESCRIBE HISTORY table_name;
````

### Query by Timestamp

```sql
SELECT * FROM table_name TIMESTAMP AS OF '2025-07-01T15:00:00';
```

### Query by Version Number

```sql
SELECT * FROM table_name VERSION AS OF 3;
-- or shorthand
SELECT * FROM table_name@v3;
```

### Restoring a Table

Restore the entire table to a previous state using:

```sql
RESTORE TABLE table_name TO TIMESTAMP AS OF '2025-07-01T15:00:00';
-- or
RESTORE TABLE table_name TO VERSION AS OF 3;
```

Use case: revert accidental deletions or schema changes.

---

## Compaction and OPTIMIZE

### Compacting Small Files

Frequent small writes create numerous small files, degrading read performance.

To compact:

```sql
OPTIMIZE table_name;
```

Delta compacts small files into larger ones to improve scan efficiency.

### Z-Order Indexing

Z-Order indexing colocates related data within the same file blocks, boosting query performance on specific columns.

#### Apply Z-Ordering

```sql
OPTIMIZE table_name ZORDER BY (column_name);
```

**Example:**

If optimized on `id`, and `id` values are uniformly distributed:

* File 1: IDs 1–50
* File 2: IDs 51–100

**Benefit:** Data skipping logic allows Spark to read only the relevant file(s) based on filter predicates.

---

## Garbage Collection with VACUUM

Delta stores obsolete data and logs to enable time travel and recovery. Over time, these files accumulate.

### Run VACUUM

```sql
VACUUM table_name RETAIN 168 HOURS;
-- or simply
VACUUM table_name;
```

* Default retention: **7 days (168 hours)**
* Files older than this are permanently deleted.

**Warning:**

> Once files are removed, you can no longer time travel to versions older than the retention threshold.

Delta protects against accidental data loss by rejecting vacuum requests for files newer than the retention period unless overridden (not recommended in production).

---

## Summary

| Feature          | Command Syntax                             | Purpose                                       |
| ---------------- | ------------------------------------------ | --------------------------------------------- |
| Time Travel      | `SELECT * FROM ... TIMESTAMP AS OF ...`    | Query historical versions                     |
|                  | `SELECT * FROM ... VERSION AS OF ...`      | Query by specific version                     |
| Restore Table    | `RESTORE TABLE TO VERSION/TIMESTAMP AS OF` | Revert table state                            |
| Compact Files    | `OPTIMIZE table_name`                      | Improve performance by reducing file count    |
| Z-Order Indexing | `OPTIMIZE ... ZORDER BY (col)`             | Accelerate filter queries on specific columns |
| Garbage Collect  | `VACUUM table_name RETAIN n HOURS`         | Remove obsolete files from storage            |

Delta Lake's advanced features empower teams to maintain performant, recoverable, and auditable data systems.
