# Core Concepts

## **Lakehouse Architecture**

A unified architecture that combines the reliability, governance, and performance of data warehouses with the openness, flexibility, and low cost of data lakes. Built around **Delta Lake**, it enables both structured and unstructured data analytics from a single platform, eliminating the data duplication and silos commonly found in traditional warehouse-lake systems.

---

## **Delta Lake**

An open-source **storage layer** that brings **ACID transactions** and **schema enforcement** to data lakes built on cloud object storage (e.g., S3, ADLS, GCS). Delta Lake is foundational to the **Lakehouse Architecture** and enables:

* **Atomicity, Consistency, Isolation, Durability (ACID)**: Ensures reliable and predictable data writes/reads even in concurrent environments.
* **Schema Enforcement**: Prevents corrupted data from entering tables by validating structure.
* **Schema Evolution**: Supports automatic or manual schema updates to adapt to changing data structures.
* **Time Travel**: Enables access to previous versions of data for debugging, auditing, and reproducibility.
* **Efficient Metadata Handling**: Uses a scalable log-based structure (`_delta_log`) to maintain transaction history without relying on metastore polling.

Delta tables can be queried using **Spark SQL** or manipulated via the DataFrame API, and they support both batch and streaming workloads.

---

## **Medallion Architecture**

A layered design pattern for structuring data processing pipelines in a Lakehouse environment:

* **Bronze Layer**: Stores raw, unvalidated data ingested directly from source systems (e.g., logs, APIs, CDC streams).
* **Silver Layer**: Applies cleansing, deduplication, joins, and enrichments to standardize the data model.
* **Gold Layer**: Contains aggregated or business-level views (e.g., KPIs, reports), often used by BI tools or downstream machine learning models.

The medallion model aligns with **ELT** workflows by loading raw data first, then applying transformations within the Lakehouse using Spark.

---

## **ELT (Extract, Load, Transform)**

A **data integration pattern** optimized for cloud-native, large-scale analytics:

1. **Extract**: Data is collected from multiple operational sources (databases, APIs, flat files, IoT streams).
2. **Load**: Raw data is ingested into **Bronze** Delta tables using scalable ingestion tools (e.g., Auto Loader, Apache Kafka).
3. **Transform**: Data is cleaned, enriched, and aggregated within the data lake using **Spark SQL** or Python, resulting in **Silver** and **Gold** datasets.

Advantages of ELT in Databricks:

* Eliminates the need for separate ETL tools.
* Leverages the scalability of distributed Spark clusters.
* Operates directly on Delta tables, minimizing data movement and duplication.
* Supports both batch and streaming pipelines via Structured Streaming.

---

## **Spark SQL**

A module in Apache Spark for querying structured data using familiar SQL syntax, enabling analysts and engineers to work on large-scale data without writing Scala or Python.

**Key features:**

* Executes distributed SQL queries on large datasets using Spark’s in-memory engine.
* Supports ANSI SQL compliance, UDFs, joins, window functions, and nested queries.
* Operates natively on **Delta Lake** tables for both read and write operations.
* Interoperable with **DataFrames**, allowing mixed SQL and programmatic transformations.

**Example:**

```sql
SELECT user_id, COUNT(*) AS sessions
FROM silver.user_activity
WHERE event_type = 'login'
GROUP BY user_id
```

Also accessible through notebooks, jobs, and dashboards within Databricks.

---

## **Unity Catalog**

A **governance and data catalog layer** for Databricks that centralizes metadata, permissions, and lineage tracking across all data assets.

**Core capabilities:**

* **Centralized Access Control**: Manages user and group permissions down to the column level across multiple workspaces.
* **Fine-Grained Permissions**: Supports RBAC for catalogs, schemas, tables, views, and functions.
* **Data Lineage**: Tracks data flow from source to output across notebooks, jobs, and dashboards.
* **Audit Logging**: Logs data access and modification events for compliance and security audits.
* **Multi-Workspace & Multi-Cloud Support**: Allows federated management of data across AWS, Azure, and GCP.

**Data hierarchy:**

```
Unity Catalog
└── Catalog (e.g., finance_catalog)
    └── Schema (e.g., transactions_schema)
        └── Table/View (e.g., daily_summary)
```

**Example Usage:**

```sql
CREATE CATALOG finance;
USE CATALOG finance;
CREATE SCHEMA transactions;
CREATE TABLE transactions.daily_summary (...);
GRANT SELECT ON TABLE transactions.daily_summary TO analyst_group;
```

Unity Catalog replaces legacy metastore-based systems with unified governance and is required for advanced compliance features like **data masking** and **row-level security**.

---

## **Workspaces**

Isolated environments within Databricks for organizing and managing team resources. Each workspace includes:

* Notebooks and dashboards
* Jobs and job definitions
* Cluster configurations
* Workspace-specific permissions
* User identities and authentication

Workspaces are often mapped to business units, teams, or projects.

---

## **Clusters**

Compute infrastructure used to run all workloads in Databricks.

* **Interactive Clusters**: Created manually for development, exploration, and testing in notebooks.
* **Job Clusters**: Auto-provisioned for scheduled or triggered workflows, terminated after execution.
* **Autoscaling & Spot Instances**: Optimize cost and performance.
* **Libraries and Init Scripts**: Support custom environments with external packages.

Clusters execute code written in notebooks, jobs, or APIs using **Spark**, with full integration into Delta Lake, Unity Catalog, and access policies.
