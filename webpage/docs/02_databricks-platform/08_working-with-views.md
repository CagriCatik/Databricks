# Working with Views

This documentation outlines how to **create**, **query**, and **observe the lifecycle** of different types of **views** in Databricks. It includes hands-on usage examples for each view type—**stored views**, **temporary views**, and **global temporary views**—along with session and cluster-level behaviors.

---

## 1. Setup: Base Table for Demonstration

Before working with views, a base table named `smartphones` is created and populated.

### 1.1. Table Creation

```sql
CREATE TABLE smartphones (
  id INT,
  name STRING,
  brand STRING,
  release_year INT
);

INSERT INTO smartphones VALUES
(1, 'iPhone X', 'Apple', 2017),
(2, 'Galaxy S10', 'Samsung', 2019),
...
(10, 'iPhone 14', 'Apple', 2023);
```

* Verifiable via:

  * **Data Explorer**
  * `SHOW TABLES` in SQL

---

## 2. Creating Views

Databricks supports three types of views. Each view is defined using a SQL `CREATE VIEW` statement with specific modifiers.

### 2.1. Stored View

#### 2.1.1. Description

* Persisted in the **metastore database** (default or user-defined).
* Accessible across **sessions and notebooks**.

#### 2.1.2. Example

```sql
CREATE VIEW view_apple_phones AS
SELECT * FROM smartphones
WHERE brand = 'Apple';
```

#### 2.1.3. Behavior

* Executes the `SELECT` query on each access.
* Confirmed via:

  * `SHOW TABLES`
  * Data Explorer (listed under default DB)
* Survives Spark session and cluster restarts.

---

### 2.2. Temporary View

#### 2.2.1. Description

* Lives only for the **current Spark session**.
* Not stored in any database.

#### 2.2.2. Example

```sql
CREATE TEMP VIEW temp_view_phones_brands AS
SELECT DISTINCT brand FROM smartphones;
```

#### 2.2.3. Behavior

* Shown in `SHOW TABLES` as `isTemporary = true`
* Not visible in Data Explorer
* Automatically removed:

  * On notebook close
  * On cluster restart
  * On interpreter restart (e.g., `pip install`)

---

### 2.3. Global Temporary View

#### 2.3.1. Description

* Lives across **sessions**, but only within the same **cluster**.
* Stored in the special **`global_temp`** database.

#### 2.3.2. Example

```sql
CREATE GLOBAL TEMP VIEW global_temp_view_latest_phones AS
SELECT * FROM smartphones
WHERE release_year > 2020
ORDER BY release_year DESC;
```

#### 2.3.3. Query Syntax

```sql
SELECT * FROM global_temp.global_temp_view_latest_phones;
```

#### 2.3.4. Behavior

* Requires `global_temp.` qualifier in queries.
* View is not listed under `SHOW TABLES` for the default database.
* View is listed using:

```sql
SHOW TABLES IN global_temp;
```

* Deleted automatically on **cluster restart**.

---

## 3. View Visibility Across Sessions

### 3.1. Stored View

* **Persisted across notebooks, sessions, and cluster restarts**.
* Found via `SHOW TABLES` and in Data Explorer.

### 3.2. Temporary View

* **Session-specific**.
* Not visible in a **new notebook** or after session reset.
* Example loss scenarios:

  * New notebook (new Spark session)
  * Detach/reattach to cluster
  * Installing Python package
  * Cluster restart

### 3.3. Global Temporary View

* **Shared across notebooks**, tied to **cluster lifecycle**.
* Visible in any notebook attached to the cluster.
* **Lost when the cluster is restarted**.

---

## 4. Cleanup Example

To remove the created objects:

```sql
DROP VIEW view_apple_phones;
DROP VIEW temp_view_phones_brands;
DROP VIEW global_temp.global_temp_view_latest_phones;
DROP TABLE smartphones;
```

---

## 5. Lifecycle Summary Table

| View Type       | Stored View             | Temporary View             | Global Temporary View                |
| --------------- | ----------------------- | -------------------------- | ------------------------------------ |
| Scope           | All sessions & clusters | Current Spark session      | All notebooks in current cluster     |
| Persistence     | Hive metastore          | In-memory                  | Cluster-level memory (`global_temp`) |
| Creation Syntax | `CREATE VIEW`           | `CREATE TEMP VIEW`         | `CREATE GLOBAL TEMP VIEW`            |
| Querying        | Regular SQL             | Regular SQL                | Use `global_temp.` prefix            |
| Visibility      | `SHOW TABLES`, Explorer | `SHOW TABLES` only         | `SHOW TABLES IN global_temp`         |
| Deletion        | Manual                  | Automatic (on session end) | Automatic (on cluster restart)       |

---

## 6. Best Practices

* Use **stored views** for reusable logic shared across all users.
* Use **temporary views** for notebook-scoped or short-lived logic.
* Use **global temporary views** for cross-notebook collaboration on the same cluster session.


