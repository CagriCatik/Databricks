# Working with Databases and Tables

This documentation details practical operations involving **databases and tables** within **Databricks**, specifically covering the Hive metastore, table creation (managed vs. external), metadata inspection, deletion behavior, and custom storage configurations. This reflects operations performed in a Databricks notebook using both SQL and the Data Explorer interface.

---

## 1. Hive Metastore Overview

### 1.1. Access via Data Explorer

* The **Hive Metastore** is visible under the **Data Explorer** in the Databricks UI.
* The **default database** (`default`) is present by default and used when no database is specified explicitly.

---

## 2. Creating and Inspecting Tables in the Default Database

### 2.1. Creating a Managed Table

```sql
CREATE TABLE managed_default (
  id INT,
  value STRING
);
```

* The `managed_default` table is created **without a LOCATION clause**, making it a **managed table**.
* Data is stored at:

  ```
  dbfs:/user/hive/warehouse/managed_default/
  ```

### 2.2. Metadata Inspection

```sql
DESCRIBE EXTENDED managed_default;
```

* Reveals:

  * `Type: MANAGED`
  * `Location: dbfs:/user/hive/warehouse/...`

### 2.3. Dropping Managed Table

```sql
DROP TABLE managed_default;
```

* Result:

  * Metadata is removed from the Hive metastore.
  * Physical files and directory are deleted from storage.

---

## 3. Creating and Managing External Tables

### 3.1. External Table Creation

```sql
CREATE TABLE external_default (
  id INT,
  value STRING
)
LOCATION '/mnt/demo/external_default';
```

* The presence of the `LOCATION` keyword classifies this as an **external table**.
* Data is stored **outside** the Hive default directory.

### 3.2. Metadata Inspection

```sql
DESCRIBE EXTENDED external_default;
```

* Confirms:

  * `Type: EXTERNAL`
  * `Location: /mnt/demo/external_default`

### 3.3. Dropping External Table

```sql
DROP TABLE external_default;
```

* Result:

  * Metadata is deleted from the Hive metastore.
  * Data files remain at `/mnt/demo/external_default`.

---

## 4. Creating Additional Databases

### 4.1. Syntax

```sql
CREATE DATABASE extra_db;
-- or
CREATE SCHEMA extra_db;
```

* Both statements are interchangeable.

### 4.2. Metadata Inspection

```sql
DESCRIBE DATABASE EXTENDED extra_db;
```

* Reveals:

  * Location: `dbfs:/user/hive/warehouse/extra_db.db/`
  * The `.db` extension is appended to distinguish database folders from table folders.

---

## 5. Working with Tables in a Custom Database

### 5.1. Set Context

```sql
USE extra_db;
```

### 5.2. Create Managed and External Tables

```sql
-- Managed Table
CREATE TABLE managed_extra (
  id INT,
  value STRING
);

-- External Table
CREATE TABLE external_extra (
  id INT,
  value STRING
)
LOCATION '/mnt/demo/external_extra';
```

### 5.3. Deletion Behavior

```sql
DROP TABLE managed_extra;
DROP TABLE external_extra;
```

* Managed table data and directory are removed.
* External table data at `/mnt/demo/external_extra` remains.

---

## 6. Creating a Database in a Custom Location

### 6.1. Syntax

```sql
CREATE DATABASE custom_db
LOCATION '/mnt/custom_databases/custom_db';
```

### 6.2. Metadata Inspection

```sql
DESCRIBE DATABASE EXTENDED custom_db;
```

* Location confirms use of the custom path.
* Metadata still managed in Hive metastore.

---

## 7. Tables in a Custom Location Database

### 7.1. Table Creation

```sql
USE custom_db;

-- Managed Table
CREATE TABLE managed_custom (
  id INT,
  value STRING
);

-- External Table
CREATE TABLE external_custom (
  id INT,
  value STRING
)
LOCATION '/mnt/demo/external_custom';
```

### 7.2. Deletion Behavior

```sql
DROP TABLE managed_custom;
DROP TABLE external_custom;
```

* **Managed Table**:

  * Metadata and data removed from custom location directory.
* **External Table**:

  * Metadata removed from Hive metastore.
  * Data at `/mnt/demo/external_custom` remains intact.

---

## 8. Summary Table

| Scope                    | Entity             | Type     | Location Behavior                                 | Drop Behavior             |
| ------------------------ | ------------------ | -------- | ------------------------------------------------- | ------------------------- |
| Default Database         | `managed_default`  | Managed  | `/user/hive/warehouse/managed_default/`           | Deletes data and metadata |
| Default Database         | `external_default` | External | `/mnt/demo/external_default/`                     | Deletes metadata only     |
| Extra Database           | `managed_extra`    | Managed  | `/user/hive/warehouse/extra_db.db/managed_extra/` | Deletes data and metadata |
| Extra Database           | `external_extra`   | External | `/mnt/demo/external_extra/`                       | Deletes metadata only     |
| Custom Location Database | `managed_custom`   | Managed  | `/mnt/custom_databases/custom_db/managed_custom/` | Deletes data and metadata |
| Custom Location Database | `external_custom`  | External | `/mnt/demo/external_custom/`                      | Deletes metadata only     |

---

## 9. Key Takeaways

* Use `DESCRIBE EXTENDED` and `DESCRIBE DATABASE EXTENDED` for detailed metadata.
* Managed tables are automatically removed along with their data.
* External tables must be manually cleaned up from the file system if needed.
* `.db` suffix helps distinguish database directories.
* The `USE` statement is required to target a specific database context during table creation.
