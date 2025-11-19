# Views

This documentation provides a detailed explanation of **views** in Databricks, covering their purpose, types, lifecycle behavior, usage patterns, and syntax. Views are fundamental for abstracting complex SQL queries and enabling reusable, logical representations of underlying data without duplicating storage.

---

## 1. What Is a View?

A **view** in Databricks is a **virtual table**:

* It **does not store physical data**.
* It represents a **saved SQL query** against one or more real tables.
* Each time the view is queried, the underlying SQL logic is re-executed.

Views simplify data access and encapsulate business logic in a reusable form.

---

## 2. Types of Views in Databricks

Databricks supports three types of views:

| View Type            | Scope                    | Persistence                  | Dropped When             | Use Case                                 |
| -------------------- | ------------------------ | ---------------------------- | ------------------------ | ---------------------------------------- |
| **Stored View**      | Across sessions & users  | Persisted in DB              | Manual (via `DROP VIEW`) | Reusable logic across notebooks          |
| **Temporary View**   | Current Spark session    | In-memory                    | On session end           | Short-term or one-time transformations   |
| **Global Temp View** | All notebooks in cluster | In-memory (`global_temp` DB) | On cluster restart       | Shared logic across notebooks in cluster |

---

## 3. Stored Views (Persistent Views)

### 3.1. Description

* Stored in the **metastore** of the target database.
* Survive across sessions and cluster restarts.
* Queryable like regular tables.

### 3.2. Syntax

```sql
CREATE VIEW sales_summary AS
SELECT region, SUM(total_sales) AS revenue
FROM sales_data
GROUP BY region;
```

### 3.3. Deletion

```sql
DROP VIEW sales_summary;
```

---

## 4. Temporary Views

### 4.1. Description

* Lives only in the **current Spark session**.
* Automatically **deleted when the session ends**.
* Commonly used for intermediate transformations or quick exploration.

### 4.2. Lifecycle Triggers

Spark session is re-initialized in the following scenarios:

* Opening a **new notebook**.
* **Detaching and reattaching** a notebook to a cluster.
* **Installing a Python package** (restarts interpreter).
* **Restarting the cluster**.

### 4.3. Syntax

```sql
CREATE TEMP VIEW temp_sales AS
SELECT * FROM sales_data WHERE region = 'EMEA';
```

* Use `TEMP` or `TEMPORARY` in the `CREATE VIEW` statement.

---

## 5. Global Temporary Views

### 5.1. Description

* Lives **across multiple sessions**, but **within the same cluster**.
* Stored in a reserved database: `global_temp`.
* Visible to all notebooks **attached to the same cluster**.

### 5.2. Syntax

```sql
CREATE GLOBAL TEMP VIEW global_sales AS
SELECT * FROM sales_data WHERE total_sales > 1000;
```

* To query:

```sql
SELECT * FROM global_temp.global_sales;
```

### 5.3. Deletion

* Automatically dropped when the **cluster restarts**.

---

## 6. Summary Table

| Feature                     | Stored View             | Temporary View       | Global Temporary View            |
| --------------------------- | ----------------------- | -------------------- | -------------------------------- |
| Data Stored                 | No                      | No                   | No                               |
| Metadata Location           | Hive Metastore          | Session memory       | `global_temp` (cluster memory)   |
| Lifetime                    | Until manually dropped  | Until session ends   | Until cluster restart            |
| Visibility Scope            | All sessions & clusters | Current session only | All sessions in same cluster     |
| Creation Syntax             | `CREATE VIEW`           | `CREATE TEMP VIEW`   | `CREATE GLOBAL TEMP VIEW`        |
| Required Qualifier to Query | None                    | None                 | `global_temp.` prefix required   |
| Use Case                    | Reusable definitions    | Quick transformation | Shared logic in dev/test cluster |

---

## 7. Best Practices

* Use **stored views** for production use cases where logic needs to persist across clusters and sessions.
* Use **temporary views** for ad hoc data exploration or transformations inside a single notebook.
* Use **global temporary views** for sharing view definitions across multiple notebooks during collaborative development in a single cluster session.
