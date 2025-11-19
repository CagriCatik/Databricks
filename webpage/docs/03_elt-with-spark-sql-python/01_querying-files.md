# Querying Files in Databricks Using Spark SQL

- This guide outlines how to extract and query data from files in Databricks using Spark SQL. 
- It includes methods for inspecting raw file content, leveraging external data sources, and loading data into Delta Lake tables using `CTAS` and `CREATE TABLE USING` statements.

---

## Basic File Querying

### Syntax

To query a file directly using Spark SQL:

```sql
SELECT * FROM format.`/path/to/file`
```

* Use **backticks (\`)** around the file path.
* Replace `format` with the appropriate file format (e.g., `json`, `parquet`).

### Supported Formats

Self-describing formats with embedded schema definitions:

* `json`
* `parquet`

Non-self-describing formats (e.g., `csv`) require additional configuration.

### Multi-File Access

You can:

* Query a single file
* Use wildcards (`*`) to access multiple files
* Query an entire directory

**Note:** All files must share the same schema and format.

---

## Raw Text and Binary Extraction

### Text Format

To load raw text content from files:

```sql
SELECT * FROM text.`/path/to/textfiles`
```

Applicable formats:

* `json`
* `csv`
* `tsv`
* `txt`

Useful for:

* Inspecting corrupted input
* Custom parsing with string functions

### Binary File Format

To load files as binary (e.g., images, unstructured data):

```sql
SELECT * FROM binaryFile.`/path/to/files`
```

---

## Creating Delta Tables from Files

### Using CTAS Statements

Create Table As Select (CTAS) allows loading file data into a Delta table:

```sql
CREATE TABLE table_name
USING DELTA
AS SELECT * FROM parquet.`/path/to/files`
```

* Schema is inferred from the `SELECT` clause.
* Data is physically moved into a managed Delta table.

### Limitations of CTAS

* **No support for schema declaration**
* **No support for file options (e.g., delimiter, header)**
* **Best used with well-defined formats** (e.g., `parquet`)

**Warning:** Not suitable for CSV ingestion due to lack of configurable options.

---

## Creating External Tables with Options

### Using `CREATE TABLE USING`

To create a table that references files directly (external table):

```sql
CREATE TABLE table_name
USING format
OPTIONS (
  key1 = 'value1',
  key2 = 'value2'
)
LOCATION '/path/to/files'
```

* Table is a **pointer** to external files.
* No data movement occurs.
* The table is **non-Delta**.
* Original file format is preserved.

### CSV External Table Example

```sql
CREATE TABLE external_csv_table
USING csv
OPTIONS (
  header = 'true',
  delimiter = ';'
)
LOCATION '/mnt/data/mycsvfiles'
```

### JDBC External Table Example

```sql
CREATE TABLE external_jdbc_table
USING jdbc
OPTIONS (
  url = 'jdbc:mysql://hostname:3306/db',
  dbtable = 'my_table',
  user = 'username',
  password = 'password'
)
```

**Note:** This points to an external SQL database table.

---

## Loading External Data into Delta Tables

To load data from an external source into a Delta table:

1. **Create a temporary view:**

```sql
CREATE OR REPLACE TEMP VIEW temp_view_name
USING csv
OPTIONS (
  header = 'true',
  delimiter = ';'
)
LOCATION '/mnt/data/mycsvfiles'
```

2. **Use CTAS to load into Delta Lake:**

```sql
CREATE TABLE delta_table
USING DELTA
AS SELECT * FROM temp_view_name
```

Benefits:

* Data is loaded and stored in Delta format.
* Full Delta Lake features are enabled (e.g., time travel, ACID).

---

## Summary

| Method                       | Data Movement | Delta Support | File Options   | Use Case                        |
| ---------------------------- | ------------- | ------------- | -------------- | ------------------------------- |
| \`SELECT \* FROM format.\`\` | No            | No            | No             | Ad-hoc querying of files        |
| `CREATE TABLE USING`         | No            | No            | Yes            | Reference external sources      |
| `CTAS`                       | Yes           | Yes           | No             | Load structured data into Delta |
| Temp View + CTAS             | Yes           | Yes           | Yes (via view) | Load external unstructured data |

**Warning:** External tables (`USING`) do not support Delta Lake features and may incur performance issues when referring to large datasets.

```
