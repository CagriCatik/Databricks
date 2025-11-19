# Querying Files Hands On

- This hands-on guide demonstrates how to use Spark SQL in Databricks notebooks to query and process raw files. 
- The exercise is based on a bookstore dataset composed of three entities: `customers`, `books`, and `orders`. You will learn how to read data files, create external and Delta tables, handle caching issues, and configure file format options.

---

## Dataset Overview

The dataset includes three logical tables:

- **customers**: JSON format
- **books**: CSV format
- **orders**: (not covered in this notebook)

Before starting, the dataset is downloaded and copied to the Databricks file system.

---

## Reading JSON Files with Spark SQL

### File Structure

- Path: `/path/to/customers`
- Format: JSON
- Number of files: 6
- Schema fields: `customer_id`, `email`, `profile`, `last_updated`

### Querying a Single JSON File

```sql
SELECT * FROM json.`/path/to/customers/export_0000.json`
````

**Note:** Use backticks (\`) around the file path.

### Querying Multiple Files with Wildcard

```sql
SELECT * FROM json.`/path/to/customers/export_*.json`
```

Returns up to 1000 records by default in preview.

### Querying All Files in a Directory

```sql
SELECT * FROM json.`/path/to/customers/`
```

* Assumes all files share the same schema and format.
* Total records: 1700 customers.

### Tracking File Origin

Add source file information using the built-in function:

```sql
SELECT input_file_name(), * FROM json.`/path/to/customers/`
```

---

## Reading Text-Based Files

### Using the `text` Format

```sql
SELECT * FROM text.`/path/to/customers/export_0000.json`
```

* Each row represents one line of text.
* Output schema: single column named `value`.
* Useful for:

  * Corrupted input
  * Manual parsing

### Using the `binaryFile` Format

```sql
SELECT * FROM binaryFile.`/path/to/customers/`
```

Output includes:

* `path`
* `modificationTime`
* `length`
* `content` (raw bytes)

---

## Reading CSV Files

### Initial Attempt (Incorrect Parsing)

```sql
SELECT * FROM csv.`/path/to/books/books.csv`
```

* Incorrect output due to:

  * Semicolon delimiter (`;`) instead of default comma (`,`).
  * Header row interpreted as data.
* Works only with self-describing formats (e.g., JSON, Parquet).

---

## Creating External Table for CSV Files

### Correct Approach Using `CREATE TABLE USING`

```sql
CREATE TABLE books (
  id INT,
  title STRING,
  author STRING,
  price DOUBLE
)
USING csv
OPTIONS (
  header = 'true',
  delimiter = ';'
)
LOCATION '/path/to/books/'
```

### Querying the External Table

```sql
SELECT * FROM books
```

* Table type: **external**
* Format: CSV (non-Delta)
* No data is moved.
* File schema and format must remain consistent.

### Metadata Inspection

```sql
DESCRIBE EXTENDED books
```

* Confirms external table status.
* Metadata includes file format and options.
* Ensures consistent parsing for future queries.

---

## Limitations of External Non-Delta Tables

* **No version guarantees**
* **No Delta Lake features** (e.g., time travel, schema enforcement)
* **Potential stale data due to caching**

---

## Example: File Addition and Cache Invalidation

### Append New Data

Use DataFrame API to write additional CSV files:

```python
books_df.write.mode("append").option("header", "true").option("delimiter", ";").csv("/path/to/books/")
```

### Count Before and After Cache Refresh

```sql
SELECT COUNT(*) FROM books
```

**Expected issue:** New rows not visible due to cache.

### Refresh the Table Cache

```sql
REFRESH TABLE books
```

**Note:** Refreshing invalidates cache and re-reads source files.

---

## Creating Delta Tables from External Sources

### Using CTAS for JSON Files

```sql
CREATE TABLE customers
USING DELTA
AS SELECT * FROM json.`/path/to/customers/`
```

* Delta table created
* Schema is auto-inferred
* Table is managed

### CTAS Limitations

* Cannot specify file options (e.g., delimiter)
* Only supports well-defined formats (e.g., JSON, Parquet)

---

## Ingesting CSV Files into Delta Table with CTAS

### Step 1: Create a Temporary View with File Options

```sql
CREATE OR REPLACE TEMP VIEW books_view
USING csv
OPTIONS (
  header = 'true',
  delimiter = ';'
)
LOCATION '/path/to/books/*.csv'
```

### Step 2: Create Delta Table from View

```sql
CREATE TABLE books_delta
USING DELTA
AS SELECT * FROM books_view
```

* Data is moved and stored in Delta format
* Table benefits from Delta features (ACID, versioning)

### Verify Delta Table

```sql
DESCRIBE EXTENDED books_delta
```

* Confirms table is in Delta format
* Ensures durable ingestion and future compatibility

---

## Summary

| Action                       | Format       | Data Moved | Delta Table | Supports Options | Recommended Use                          |
| ---------------------------- | ------------ | ---------- | ----------- | ---------------- | ---------------------------------------- |
| \`SELECT \* FROM format.\`\` | Any          | No         | No          | No               | Quick file inspection                    |
| `CREATE TABLE USING`         | Any          | No         | No          | Yes              | External references with schema control  |
| `CTAS`                       | Parquet/JSON | Yes        | Yes         | No               | Ingest well-structured data into Delta   |
| Temp View + CTAS             | Any          | Yes        | Yes         | Yes              | Ingest option-sensitive formats like CSV |

**Note:** Use Delta format for performance, reliability, and feature support.


