# Understanding Delta Tables

- This notebook introduces the fundamentals of working with Delta Lake tables in Databricks, including creation, data insertion, updates, file structure, and transaction logging using the Hive Metastore.

---

## Catalog and Metadata Configuration

Delta tables in Databricks reside within a **catalog structure**. Databricks supports:

- **Unity Catalog** (recommended, full governance features)
- **Hive Metastore** (used here for simplicity)

Configure the current notebook to use the Hive Metastore:

```sql
USE CATALOG hive_metastore;
```

All subsequent table operations will use this catalog.

---

## Creating Delta Tables

Delta is the default format on Databricks. The following command creates a Delta table:

```sql
CREATE TABLE employees (
  id INT,
  name STRING,
  salary DOUBLE
);
```

The table is visible under `hive_metastore.default.employees`.

You can inspect it via the Catalog Explorer to confirm:

* Table format: Delta
* Columns: `id`, `name`, `salary`

---

## Inserting Data

Insert multiple records using standard SQL syntax:

```sql
INSERT INTO employees VALUES (1, 'Adam', 1000);
INSERT INTO employees VALUES (2, 'Anna', 1200);
INSERT INTO employees VALUES (3, 'Bob', 1100);
INSERT INTO employees VALUES (4, 'Bella', 1150);
```

Each `INSERT` triggers a separate **transaction**, resulting in one Parquet data file per statement.

---

## Querying Data

Query the table using:

```sql
SELECT * FROM employees;
```

Only the result of the **last SQL statement** in a cell will be displayed unless explicitly separated.

---

## Inspecting Table Metadata

Use the following command to retrieve table-level metadata:

```sql
DESCRIBE DETAIL employees;
```

Important fields include:

* `location`: path to the table storage
* `numFiles`: number of current data files
* `format`: Delta
* `tableType`: managed

List files in the location using Databricks File System magic:

```python
%fs ls dbfs:/path/to/employees/
```

Expected contents:

* Four `.parquet` files
* `_delta_log/` directory

---

## Update Operations and File Behavior

Update records using standard SQL:

```sql
UPDATE employees
SET salary = salary + 100
WHERE name LIKE 'A%';
```

This affects rows with names starting with 'A' (Adam, Anna).

**Important Notes:**

* Delta **does not modify** existing files
* **New files** are written with updated data
* **Old files** are logically removed (soft delete)

Re-inspect metadata:

```sql
DESCRIBE DETAIL employees;
```

Although six files exist (original + updated), only **four** are considered active.

---

## Transaction Log and Table History

Delta Lake maintains a full **audit trail** using a transaction log stored in `_delta_log`.

Inspect the table history:

```sql
DESCRIBE HISTORY employees;
```

Example history breakdown:

| Version | Operation | Description          |
| ------- | --------- | -------------------- |
| 0       | CREATE    | Table creation       |
| 1–4     | INSERT    | Four data insertions |
| 5       | UPDATE    | Salary update        |

Inspect log directory:

```python
%fs ls dbfs:/path/to/employees/_delta_log/
```

Each transaction corresponds to a JSON file: `000000.json`, `000001.json`, ..., `000005.json`

Inspect the latest JSON log:

* `"add"`: new files created in update
* `"remove"`: old files marked obsolete

These files are **immutable**; Delta ensures atomicity by versioning changes.

---

## Summary

| Action          | Behavior in Delta Table                           |
| --------------- | ------------------------------------------------- |
| Table Creation  | Parquet format + initialized `_delta_log`         |
| Data Insertion  | New file + transaction log entry per insert       |
| Data Update     | New file(s) added, old file(s) marked as removed  |
| Query Execution | Uses transaction log to find active (valid) files |
| Metadata Access | Via `DESCRIBE DETAIL` and `DESCRIBE HISTORY`      |
| Audit Trail     | Maintained in `_delta_log` as JSON-formatted logs |

Delta Lake’s transaction log is the backbone enabling ACID compliance, time travel, and safe concurrent operations.


## ACID Transactions

ACID is an acronym representing four key properties—**Atomicity**, **Consistency**, **Isolation**, and **Durability**—that guarantee reliable processing of database transactions. These properties are critical for ensuring data integrity, especially in systems where reliability and correctness are paramount.

### Atomicity

Atomicity ensures that each transaction is treated as a single, indivisible unit of work. This means:

- Either all operations within the transaction are executed successfully, or none are.
- If any operation fails, the entire transaction is rolled back.
- The database remains unchanged if the transaction does not complete fully.

> Example: In a banking system, transferring money involves debiting one account and crediting another. If either operation fails, the transaction is aborted and the database is restored to its previous state.

### Consistency

Consistency guarantees that a transaction takes the database from one valid state to another. It enforces database constraints, rules, and triggers, ensuring:

- No violation of data integrity or business rules.
- Data remains valid before and after a transaction.

> Example: If a table requires that account balances be non-negative, a transaction that would result in a negative balance will be rejected to maintain consistency.

### Isolation

Isolation ensures that concurrent transactions do not interfere with one another. Each transaction operates as if it is the only one executing, even when many are processed simultaneously. This prevents:

- Dirty reads
- Lost updates
- Non-repeatable reads

Most database systems offer isolation levels (e.g., Read Committed, Repeatable Read, Serializable) to balance consistency and performance.

> Example: If two users attempt to update the same account balance at the same time, isolation ensures their transactions do not conflict or produce incorrect results.

### Durability

Durability guarantees that once a transaction is committed:

- Its changes are permanently recorded in the database.
- The results are preserved even in the event of a system crash, power failure, or hardware issue.

> Example: After confirming a successful funds transfer, the updated balances remain stored even if the server goes offline immediately afterward.

### Importance

ACID properties are foundational to transactional systems such as:

- Banking and financial services
- E-commerce platforms
- Inventory and order management systems
- Software-as-a-Service (SaaS) backends

By ensuring correctness, reliability, and recoverability, ACID transactions provide the consistency required to build dependable and trustworthy data systems.
