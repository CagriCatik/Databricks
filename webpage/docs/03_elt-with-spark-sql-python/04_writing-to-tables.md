# Writing Tables Hands On

- This chapter explains how to write, update, and manage data in Delta tables using Spark SQL in Databricks. 
- You will learn how to overwrite, append, and upsert records with ACID-compliant operations. All examples are demonstrated using the bookstore dataset.

---

## Creating Delta Tables

To begin, create a Delta table using a `CTAS` statement from well-structured source files (e.g., Parquet):

```sql
CREATE TABLE orders
USING DELTA
AS SELECT * FROM parquet.`/path/to/orders/`
````

* The table will be managed.
* Schema is auto-inferred from Parquet.

---

## Overwriting Table Data

### Method 1: CREATE OR REPLACE TABLE

```sql
CREATE OR REPLACE TABLE orders
AS SELECT * FROM parquet.`/path/to/orders-new/`
```

* Fully replaces table content.
* Schema can change.
* Generates a new version in the table's history.

**Advantages:**

* Time Travel support for previous versions
* Atomic write operation
* No recursive directory deletion
* Old data is retained

### Table History Inspection

```sql
DESCRIBE HISTORY orders
```

---

### Method 2: INSERT OVERWRITE

```sql
INSERT OVERWRITE orders
SELECT * FROM parquet.`/path/to/orders-updated/`
```

* Replaces existing table content.
* Must match current schema.
* Does not create new tables.

**Advantages:**

* Schema enforcement
* Prevents unintended schema changes
* Creates a new version in table history

### History Confirmation

```sql
DESCRIBE HISTORY orders
```

---

### Schema Enforcement Differences

If schema mismatch occurs (e.g., added column):

```sql
INSERT OVERWRITE orders
SELECT *, current_timestamp() AS modified_at
FROM parquet.`/path/to/orders-updated/`
```

**Error:**

> A schema mismatch detected when writing to the Delta table

* `INSERT OVERWRITE` enforces strict schema match
* `CREATE OR REPLACE` allows schema evolution

---

## Appending New Records

### INSERT INTO

```sql
INSERT INTO orders
SELECT * FROM parquet.`/path/to/orders-new/`
```

* Adds new rows to the existing table.
* Total count increases.
* Simple and fast operation.

**Warning:** Does not prevent duplicates. Re-running will duplicate records.

---

## Merging Records (Upserts)

### MERGE INTO Customers Table

Used to update existing records and insert new ones from a source view.

#### Step 1: Create Temporary View

```sql
CREATE OR REPLACE TEMP VIEW customer_updates
AS
SELECT * FROM json.`/path/to/customers-updated.json`
```

#### Step 2: Perform Merge

```sql
MERGE INTO customers AS target
USING customer_updates AS source
ON target.customer_id = source.customer_id
WHEN MATCHED AND target.email IS NULL AND source.email IS NOT NULL THEN
  UPDATE SET target.email = source.email,
             target.last_updated = current_timestamp()
WHEN NOT MATCHED THEN
  INSERT *
```

**Results:**

* 100 rows updated
* 201 rows inserted
* 0 rows deleted

**Note:** Operation is atomic and ACID-compliant.

---

### MERGE INTO Books Table

Filter records before inserting to avoid duplicates and apply custom logic.

#### Step 1: Create Temporary View

```sql
CREATE OR REPLACE TEMP VIEW books_updates
AS
SELECT * FROM csv.`/path/to/books-new.csv`
```

#### Step 2: Merge With Conditional Insert

```sql
MERGE INTO books AS target
USING books_updates AS source
ON target.book_id = source.book_id AND target.title = source.title
WHEN NOT MATCHED AND source.category = 'Computer Science' THEN
  INSERT *
```

**Results:**

* 3 new books inserted (category: Computer Science)

#### Idempotency Check

Re-running the same merge:

```sql
MERGE INTO books ...
```

**Result:**

> 0 records inserted — duplicates prevented.

---

## Summary

| Operation              | Statement                 | Schema Change | Prevents Duplicates | Notes                                        |
| ---------------------- | ------------------------- | ------------- | ------------------- | -------------------------------------------- |
| Overwrite Table        | `CREATE OR REPLACE TABLE` | Yes           | No                  | Allows schema evolution                      |
| Overwrite Table        | `INSERT OVERWRITE`        | No            | No                  | Strict schema match                          |
| Append Records         | `INSERT INTO`             | No            | No                  | Fast but not idempotent                      |
| Upsert (Insert/Update) | `MERGE INTO`              | No            | Yes                 | Best for deduplication and conditional logic |

**Note:** Delta Lake enables reliable, performant table writes through transactional guarantees and table versioning.

