# Databricks Lakehouse Platform

The Databricks Lakehouse Platform is a multi-cloud data platform based on Apache Spark. It unifies data engineering, data science, analytics, and machine learning (ML) using the **Lakehouse architecture**. This model combines the openness and flexibility of data lakes with the governance and performance of data warehouses.

---

## 1. Lakehouse Architecture

### Characteristics

A **Lakehouse** architecture integrates features from both data lakes and data warehouses:

- **Data Lake Capabilities**:
  - Schema-on-read
  - Storage of raw or semi-structured data
  - Support for ML and AI tooling
  - Use of open file formats (e.g., Parquet, ORC)

- **Data Warehouse Capabilities**:
  - ACID transactions
  - Data indexing and caching
  - Fine-grained access control
  - BI performance optimizations

### Use Cases

- Unified ETL/ELT pipelines
- Interactive dashboards
- Advanced analytics
- Machine learning model development and training

---

## 2. Platform Architecture

Databricks is structured across three primary architectural layers:

### 2.1 Cloud Service Layer

- **Purpose**: Manages cloud infrastructure integration and centralized services.
- **Functions**:
  - Workspace orchestration
  - Authentication and identity management
  - Web-based UI delivery
  - Job and cluster lifecycle management
- **Deployment Options**: AWS, Azure, Google Cloud Platform

### 2.2 Databricks Runtime

- **Components**:
  - Apache Spark
  - Delta Lake
  - Built-in system libraries
- **Features**:
  - Pre-configured on all compute clusters
  - Optimized for high-performance batch and stream processing
  - Native support for:
    - **Languages**: SQL, Python, Scala, Java, R
    - **Workloads**: ETL, ML, BI, streaming

### 2.3 Databricks Workspace

- **Purpose**: Central environment for collaborative development.
- **Capabilities**:
  - Interactive notebooks
  - Versioned job workflows
  - Visualizations and dashboards
  - Code and model versioning

---

## 3. Control Plane vs Data Plane

Databricks operates under a **shared responsibility model** that separates the control plane and the data plane.

### 3.1 Control Plane (Databricks Managed)

- Hosted in the Databricks cloud account
- Contains:
  - Web UI
  - Job and cluster managers
  - Notebooks
  - Orchestration and scheduling tools

### 3.2 Data Plane (Customer Managed)

- Deployed in the customer’s cloud account
- Contains:
  - Virtual machines for compute
  - Cloud-native object storage (e.g., S3, ADLS, GCS)
  - Spark drivers and executors
  - DBFS (Databricks File System)

> **Note**: All compute and data operations occur in the customer’s infrastructure. Databricks cannot access customer data directly.

---

## 4. Databricks File System (DBFS)

### Definition

DBFS is a distributed file abstraction layer that sits atop cloud storage systems, making data accessible to Spark workloads within Databricks clusters.

### Features of DBFS

- **Auto-Mounted**: Available on every cluster without additional configuration.
- **Persistent**: Data written to `dbfs:/` paths persists independently of cluster shutdown.
- **Unified Access**: Supports interaction with local, cloud, and mounted external storage.

### Example

```sql
-- Store a CSV file to DBFS
COPY INTO 'dbfs:/mnt/mydata/data.csv'
FROM 's3://mybucket/data.csv'
FILEFORMAT = CSV;
````

---

## 5. Delta Lake Integration

### Overview

**Delta Lake** is a storage layer built on top of Parquet that brings ACID transactions and schema enforcement to data lakes.

### Core Capabilities

- Atomic writes and transactional consistency
- Time travel with data versioning
- Schema evolution and enforcement
- Scalable metadata handling

### Example: Creating a Delta Table

```sql
CREATE TABLE delta_table
USING DELTA
LOCATION 'dbfs:/mnt/delta/my_table'
AS
SELECT * FROM parquet.`dbfs:/mnt/raw/input_data`;
```

---

## 6. Apache Spark Integration

Databricks is tightly integrated with Apache Spark and provides an optimized runtime.

### Features of Apache Stark

- In-memory distributed computation
- DAG-based execution engine
- Adaptive query execution
- Support for Spark SQL, MLlib, GraphX, Structured Streaming

### Supported Data Types

- **Structured**: CSV, Parquet, Avro
- **Semi-structured**: JSON, XML
- **Unstructured**: Images, video, text blobs

---

## 7. SQL Operations in Databricks

### CTAS (Create Table As Select)

Creates a new table from a SELECT query.

```sql
CREATE TABLE sales_summary
USING DELTA
AS
SELECT product_id, SUM(revenue) AS total_revenue
FROM sales_data
GROUP BY product_id;
```

> **Note**: CTAS does not support partitioning or other advanced options in some runtime versions. Use `CREATE TABLE ... LOCATION` and `INSERT INTO` as an alternative when needed.

### DDL and DML Support

Databricks supports full SQL capabilities including:

- **DDL**:

  - `CREATE TABLE`
  - `ALTER TABLE`
  - `DROP TABLE`

- **DML**:

  - `INSERT INTO`
  - `MERGE INTO`
  - `DELETE`, `UPDATE`

### Example: MERGE INTO

```sql
MERGE INTO target_table AS t
USING updates_table AS u
ON t.id = u.id
WHEN MATCHED THEN UPDATE SET t.value = u.value
WHEN NOT MATCHED THEN INSERT (id, value) VALUES (u.id, u.value);
```

---

## 8. Streaming Workloads

Databricks supports real-time processing via **Structured Streaming** using both SQL and APIs.

### Example: Read Stream

```sql
CREATE OR REPLACE TEMP VIEW live_data
USING cloudFiles
OPTIONS (
  path "dbfs:/mnt/streaming/input/",
  format "json"
);
```

### Example: Write Stream

```sql
CREATE STREAMING LIVE TABLE cleaned_data
AS
SELECT *
FROM STREAM(live_data)
WHERE is_valid = TRUE;
```

---

## Summary

Databricks provides an end-to-end, scalable Lakehouse platform with the following benefits:

- Combines data warehouse reliability and performance with data lake flexibility
- Native integration with Delta Lake and Apache Spark
- Multi-language support for collaborative development
- Secure separation of control and data planes
- Powerful support for both batch and streaming workloads

Databricks enables organizations to unify data storage, processing, analytics, and AI development in a secure, governed, and high-performance environment
