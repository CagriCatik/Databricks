# Relational Entities

This document explains the architecture and behavior of **relational entities** in **Databricks**, focusing on **databases**, **tables**, **storage management**, and the impact of the `LOCATION` keyword. It covers internal mechanisms such as the **Hive metastore**, and provides definitions, lifecycle details, and usage scenarios for both **managed** and **external** tables.

---

## 1. Hive Metastore in Databricks

### 1.1. Purpose

Databricks uses a **Hive metastore** as the central repository for **metadata**. This includes information about:

* Databases (schemas)
* Tables (definitions, types)
* Partitions
* Data formats
* Storage paths

### 1.2. Workspace Scope

* Every **Databricks workspace** is linked to a **central Hive metastore**.
* All clusters in the workspace can **access shared metadata** via this metastore.

---

## 2. Databases in Databricks

### 2.1. Terminology

* In Databricks, a **database** is equivalent to a **schema** in Hive terminology.
* You can use either:

  * `CREATE DATABASE db_name`
  * `CREATE SCHEMA db_name`
    Both are functionally identical.

### 2.2. Default Database

* Databricks provides a default database named **`default`**.
* Creating a table without specifying a database places it under this default schema.
* Default storage path:
  `dbfs:/user/hive/warehouse/`

### 2.3. Custom Databases

* You can create additional databases using:

  ```sql
  CREATE DATABASE db_name;
  ```
* Each database will have a directory created at:
  `dbfs:/user/hive/warehouse/db_name.db/`

### 2.4. Custom Storage Location

* You can override the default location using the `LOCATION` keyword:

  ```sql
  CREATE SCHEMA db_name LOCATION '/mnt/external_path/db_name';
  ```
* Metadata remains in the Hive metastore.
* Table data will be stored in the **custom specified path**.

---

## 3. Tables in Databricks

### 3.1. Types of Tables

#### 3.1.1. Managed Tables

* Created **inside the database's storage directory**.
* Lifecycle managed by Hive metastore.
* Dropping the table removes:

  * Metadata
  * **Physical data files**

#### 3.1.2. External Tables

* Created with data stored in an **external location**, specified with `LOCATION`.
* Only the **metadata** is managed by the Hive metastore.
* Dropping the table removes:

  * **Only metadata**
  * **Data files remain** intact.

### 3.2. Creating Tables

#### 3.2.1. Managed Table (Default Behavior)

```sql
CREATE TABLE table_name (
  id INT,
  name STRING
);
```

* Metadata stored in Hive under selected database.
* Data stored in `/user/hive/warehouse/db_name.db/table_name/`.

#### 3.2.2. External Table in Default Database

```sql
CREATE TABLE table_name (
  id INT,
  name STRING
)
LOCATION '/mnt/external_data/table_data/';
```

* Metadata in Hive under `default`.
* Data stored in specified external location.

#### 3.2.3. External Table in Custom Database

```sql
USE custom_db;

CREATE TABLE ext_table (
  id INT,
  value STRING
)
LOCATION '/mnt/another_path/external_table/';
```

* Database may reside in default or custom location.
* Table metadata stored in Hive metastore under `custom_db`.
* Data files stored in external specified location.

---

## 4. Summary of Storage Logic

| Entity Type        | Metadata Location | Data Storage Location                     | Deletion Behavior        |
| ------------------ | ----------------- | ----------------------------------------- | ------------------------ |
| Managed Table      | Hive Metastore    | Under database folder (default or custom) | Deletes metadata & files |
| External Table     | Hive Metastore    | External path (via `LOCATION`)            | Deletes metadata only    |
| Database (Default) | Hive Metastore    | `/user/hive/warehouse/db_name.db/`        | Standard Hive behavior   |
| Database (Custom)  | Hive Metastore    | As specified by `LOCATION`                | Files retained manually  |

---

## 5. Example Workflow in SQL

```sql
-- Create a database in default location
CREATE DATABASE finance;

-- Create a database in custom location
CREATE SCHEMA analytics LOCATION '/mnt/data/analytics_db';

-- Use the custom database
USE analytics;

-- Create a managed table
CREATE TABLE managed_table (
  id INT,
  value STRING
);

-- Create an external table
CREATE TABLE external_table (
  id INT,
  value STRING
)
LOCATION '/mnt/data/external_table';
```

---

## 6. Important Considerations

* Use `LOCATION` only when you want fine control over physical data storage.
* Use **managed tables** when you want Databricks to fully manage table lifecycle.
* Use **external tables** when:

  * Data is shared across environments.
  * You want to retain the data post-table drop.
  * Data exists prior to table creation.

---

## 7. Next Steps

You can now experiment with relational entities in **Databricks notebooks** using SQL or PySpark, with an understanding of how metadata and data are handled in the platform.
