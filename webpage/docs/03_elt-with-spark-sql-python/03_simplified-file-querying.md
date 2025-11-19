# Simplified File Querying with `read_files`

- Databricks introduced a new Spark SQL function called `read_files` that simplifies querying CSV and other file formats. 
- It eliminates the need to create a temporary view when ingesting file-based data for analysis or table creation.

---

## Overview

The `read_files` function supports direct access to file content with optional parsing configurations. It is particularly useful for:

- Ad-hoc queries on external files
- CTAS operations
- Simplifying schema management

---

## Example: Querying CSV Files

The following example reads multiple CSV files matching a pattern:

```sql
SELECT * FROM read_files(
  '${dataset_bookstore}/books-csv/export_*.csv',
  format => 'csv',
  header => 'true',
  delimiter => ';'
)
````

This produces a tabular result where each row corresponds to a line in the CSV files, parsed according to the provided options.

---

## Creating Delta Tables Using `read_files`

`read_files` can be used as the source in a `CREATE TABLE AS SELECT` (CTAS) operation:

```sql
CREATE TABLE books
AS SELECT * FROM read_files(
  '${dataset_bookstore}/books-csv/export_*.csv',
  format => 'csv',
  header => 'true',
  delimiter => ';'
)
```

* The resulting table is a **Delta table**.
* Schema is inferred automatically from the input files.

---

## Schema Inference and `_rescued_data`

The `read_files` function attempts to infer a unified schema across all source files. If any row does not conform to the expected schema, the raw content is captured in an additional column named `_rescued_data`.

### Example Scenario

Source file with malformed or mismatched data:

```
;;Computer Science;530
Computer Science;49
```

Query output:

| category         | price | \_rescued\_data                              |
| ---------------- | ----- | -------------------------------------------- |
| Computer Science | 44    | null                                         |
| Computer Science | 38    | null                                         |
| Computer Science | null  | {"price":"530", "\_file\_path":"dbfs\:/..."} |
| Computer Science | 49    | null                                         |

* The malformed row is captured under `_rescued_data` as a JSON string.
* This allows inspection or remediation of bad records without failing the entire query.

---

## Further Documentation

Refer to the [Databricks documentation on read\_files](https://docs.databricks.com/sql/language-manual/functions/read_files.html) for detailed syntax and supported options.
