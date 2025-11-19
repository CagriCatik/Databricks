# Setting Up Delta Tables

This document provides detailed coverage of working with **Delta Lake tables** in Databricks. It focuses on creating Delta tables using **CTAS statements**, enforcing **table constraints**, and creating **clones** (deep or shallow) of Delta tables. It also highlights best practices and the comparative features of CTAS and regular table creation methods.

---

## 1. Creating Delta Tables with CTAS

### 1.1. What Is CTAS?

**CTAS (Create Table As Select)** is a SQL statement used to:

* Create a new Delta table.
* Automatically populate the table with data from a `SELECT` query.

### 1.2. Key Characteristics

* **Schema inference**: Schema is derived from the SELECT statement. You cannot manually declare column types.
* **Immediate data population**: Unlike regular `CREATE TABLE`, CTAS inserts data during creation.
* **Supports transformations**:

  * Rename columns.
  * Select subset of columns.

### 1.3. Example

```sql
CREATE TABLE user_info
COMMENT 'Contains PII (name, email)'
PARTITIONED BY (city, birthdate)
LOCATION '/mnt/external_data/user_info'
AS
SELECT 
  id,
  name AS full_name,
  email,
  city,
  birthdate
FROM raw_users;
```

* `COMMENT`: Documents the table content.
* `PARTITIONED BY`: Organizes data in subfolders by partition keys.
* `LOCATION`: Stores table data at a specified external location.

---

## 2. CTAS vs. Regular CREATE TABLE

| Feature                | CTAS                    | Regular CREATE TABLE             |
| ---------------------- | ----------------------- | -------------------------------- |
| Schema Declaration     | Inferred from SELECT    | Must be declared manually        |
| Data Insertion         | Immediate (from SELECT) | Requires `INSERT INTO` afterward |
| Partition Support      | Supported               | Supported                        |
| External Storage       | Via `LOCATION`          | Via `LOCATION`                   |
| Column Transformations | Inline via SELECT       | Not applicable at creation       |

---

## 3. Partitioning Best Practices

### 3.1. When to Partition

* **Recommended** for large Delta tables to enhance query performance.
* **Avoid** for small/medium tables due to:

  * File fragmentation.
  * Reduced file compaction efficiency.
  * Ineffective data skipping.

### 3.2. Syntax Example

```sql
PARTITIONED BY (region, registration_date)
```

---

## 4. Adding Table Constraints

Delta tables support **data integrity constraints**, which are enforced during data writes.

### 4.1. Supported Constraint Types

* `NOT NULL`
* `CHECK` (logical condition enforcement)

### 4.2. Constraint Requirements

* **Existing data** must conform to the constraint before applying.
* **Violations** on insert/update operations will trigger write failure.

### 4.3. Example: Adding a CHECK Constraint

```sql
ALTER TABLE customers
ADD CONSTRAINT chk_valid_date
CHECK (registration_date >= '2023-01-01');
```

* Constraints are similar in syntax to `WHERE` clauses.

---

## 5. Copying Delta Tables (Cloning)

Delta Lake supports two cloning methods: **deep** and **shallow**.

### 5.1. Deep Clone

#### 5.1.1. Behavior

* Full copy of:

  * **Data**
  * **Metadata**
* Suitable for:

  * Backup
  * Long-term duplication
  * Full environment replication

#### 5.1.2. Syntax

```sql
CREATE TABLE users_backup
DEEP CLONE users;
```

* Can be re-run to **sync changes incrementally**.
* Time-intensive for large tables.

### 5.2. Shallow Clone

#### 5.2.1. Behavior

* Copies only the **Delta transaction log**.
* No data movement.
* Fast operation.
* Ideal for:

  * Testing
  * Development environments
  * Sandboxing

#### 5.2.2. Syntax

```sql
CREATE TABLE users_test
SHALLOW CLONE users;
```

### 5.3. Isolation and Data Integrity

* **All modifications** to cloned tables are **isolated**.
* Source tables remain unaffected by changes to clones.

---

## 6. Summary

| Feature          | CTAS            | Regular CREATE | Deep Clone           | Shallow Clone              |
| ---------------- | --------------- | -------------- | -------------------- | -------------------------- |
| Data Insert      | During creation | Manual insert  | Full data + metadata | Metadata only              |
| Schema           | Inferred        | Manual         | Cloned               | Cloned                     |
| Partitioning     | Supported       | Supported      | Preserved            | Preserved                  |
| External Storage | Via `LOCATION`  | Supported      | Optional             | Optional                   |
| Use Case         | Transform+load  | Schema setup   | Backup/replica       | Fast development/test copy |
| Data Movement    | Yes             | N/A            | Yes                  | No                         |

---

## 7. Recommendations

* Prefer **CTAS** for quick data ingestion from existing tables.
* Use **partitioning only for large datasets**.
* Apply **constraints** to enforce business rules at the storage level.
* Use **deep clones** for full-scale duplication and backup.
* Use **shallow clones** for non-invasive dev/test scenarios.
