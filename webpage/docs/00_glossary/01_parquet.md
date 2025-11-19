# Apache Parquet

Apache Parquet is a **columnar storage file format** designed for efficient data storage and retrieval, especially for analytical workloads. It is open source and widely supported across big data tools. 

>TLDR;

* Parquet is **optimized for analytics**: columnar, compressed, self-describing, and schema-aware.
* It significantly **reduces storage** and **speeds up columnar queries** compared to CSV/JSON.
* Works best when data is large, structured, and queried by column subsets.

---

## Core Characteristics

* **Columnar Storage**
  Data is stored **column by column**, unlike row-based formats (e.g., CSV). Queries that read only a few columns can skip the rest, saving I/O and memory.

* **Efficient Compression & Encoding**
  Each column can use a compression and encoding strategy suited to its data type (e.g., dictionary encoding for strings, run-length encoding for repeated values).

* **Schema Evolution**
  The file includes the schema. You can add or remove columns later without rewriting the entire dataset.

* **Cross-Language & Tool Support**
  Supported in **Apache Spark**, **Hive**, **Presto/Trino**, **Drill**, **Flink**, **Dremio**, **BigQuery**, and libraries like **PyArrow** and **pandas**.

* **Self-Describing**
  Metadata (schema, column statistics, min/max values, compression type) is embedded in the file, helping query engines optimize access.

---

## Advantages Compared to Other Formats

| Feature                    | Parquet                        | CSV                  | JSON                   | Avro      |
| -------------------------- | ------------------------------ | -------------------- | ---------------------- | --------- |
| **Storage Type**           | Columnar                       | Row-based            | Row-based              | Row-based |
| **Compression Efficiency** | High (per-column encoding)     | Low                  | Moderate               | Moderate  |
| **Schema Support**         | Yes                            | No                   | Weak (implicit)        | Strong    |
| **Read Performance**       | Very fast for column subset    | Slow (full row read) | Slow (full parse)      | Moderate  |
| **Write Performance**      | Moderate                       | Fast                 | Fast                   | Fast      |
| **Query Optimization**     | Predicate pushdown, statistics | None                 | None                   | Limited   |
| **Data Type Support**      | Rich (nested, arrays, structs) | Strings only         | Nested but inefficient | Rich      |

**Key Takeaways:**

* **Parquet vs CSV**: Parquet compresses far better and only reads needed columns; CSV must scan all columns.
* **Parquet vs JSON**: Parquet is binary and structured; JSON is text-based and slower to parse.
* **Parquet vs Avro**: Avro is better for streaming and row-oriented use cases; Parquet excels in analytics and querying subsets of columns.

---

## Practical Examples

### Python (pandas + PyArrow)

```python
import pandas as pd

# Write to Parquet
df = pd.DataFrame({
    "user_id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "score": [95.5, 88.0, 92.3]
})
df.to_parquet("data.parquet", engine="pyarrow", compression="snappy")

# Read Parquet
df2 = pd.read_parquet("data.parquet", engine="pyarrow")
print(df2)
```

### Apache Spark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ParquetExample").getOrCreate()
df = spark.read.parquet("s3://my-bucket/data.parquet")
df.select("user_id", "score").filter(df.score > 90).show()
```

### DuckDB (ad-hoc querying)

```sql
SELECT user_id, score
FROM 'data.parquet'
WHERE score > 90;
```

---

## When to Use Parquet

* **Data Lakes / Warehouses** (e.g., on S3, GCS, Azure Blob)
* **Analytics with Spark, Trino, Presto**
* **ETL Pipelines** needing schema evolution and compression
* **Machine Learning Feature Storage**

Avoid Parquet if:

* You need **fast row-based writes** (e.g., transactional logs).
* Data is very small and human-readable inspection matters (CSV/JSON may be simpler).

---

## Primary / Authoritative Sources

1. **Apache Parquet Documentation (official)** — overview, file format specs, internals
   [https://parquet.apache.org/docs/](https://parquet.apache.org/docs/) ([Apache Parquet][1])

2. **Parquet Format GitHub / Specification (Thrift definitions etc.)**
   [https://github.com/apache/parquet-format](https://github.com/apache/parquet-format) ([GitHub][2])

3. **Apache Parquet — File Format section (metadata, column chunks etc.)**
   [https://parquet.apache.org/docs/file-format/](https://parquet.apache.org/docs/file-format/) ([Apache Parquet][3])

4. **Apache Parquet — Types supported**
   [https://parquet.apache.org/docs/file-format/types/](https://parquet.apache.org/docs/file-format/types/) ([Apache Parquet][4])

---

## Comparative / Research / Analysis Papers & Articles

1. *An Empirical Evaluation of Columnar Storage Formats* — benchmark and comparison of Parquet vs ORC under modern workloads ([arXiv][5])
2. *High-Performance Data Storage: A Comparative Analysis of AVRO, Parquet, ORC* — comparing Parquet with Avro & ORC in big data systems ([espjeta.org][6])
3. *Big Data File Formats: Evolution, Performance, and the Rise of Columnar* — history, tradeoffs, analysis ([ijsat.org][7])
4. *Mastering Big Data Formats: ORC, Parquet, Avro, Iceberg, …* — comparative analysis and decision criteria ([Seventh Sense Research Group®][8])

---

## Comparison / Tutorial Articles

1. *Avro vs. Parquet: A Complete Comparison for Big Data Storage* (DataCamp blog) ([DataCamp][9])
2. *CSV vs Parquet vs Avro: Choosing the Right Tool for the Right Job* ([Read Medium articles with AI][10])
3. *Parquet, ORC, and Avro: The File Format Fundamentals of Big Data* (Upsolver blog) ([Upsolver][11])
4. *Choosing the Right File Format for Big Data* (Ghost in the Data) ([ghostinthedata.info][12])
5. *StackOverflow discussion: “Why Avro or Parquet faster than CSV?”* ([Stack Overflow][13])
6. *StackOverflow: Pros and cons of Parquet vs other formats* ([Stack Overflow][14])
7. *GeekLogBook — Differences between Parquet, Avro, JSON, CSV* ([geeklogbook.com][15])

---

If you like, I can collect a PDF “reading pack” (some papers + articles) and send you links or summaries.

[1]: https://parquet.apache.org/docs "Documentation - Apache Parquet"
[2]: https://github.com/apache/parquet-format "GitHub - apache/parquet-format: Apache Parquet Format"
[3]: https://parquet.apache.org/docs/file-format "File Format - Apache Parquet"
[4]: https://parquet.apache.org/docs/file-format/types "Types - Apache Parquet"
[5]: https://arxiv.org/abs/2304.05028 "An Empirical Evaluation of Columnar Storage Formats"
[6]: https://www.espjeta.org/Volume4-Issue3/JETA-V4I3P117.pdf "High-Performance Data Storage: A Comparative Analysis of AVRO, Parquet ..."
[7]: https://www.ijsat.org/papers/2020/3/1165.pdf "Big Data File Formats: Evolution, Performance, and the Rise of Columnar ..."
[8]: https://ijcttjournal.org/2025/Volume-73%20Issue-1/IJCTT-V73I1P105.pdf "Mastering Big Data Formats: ORC, Parquet, Avro, Iceberg, and the ..."
[9]: https://www.datacamp.com/blog/avro-vs-parquet "Avro vs. Parquet: A Complete Comparison for Big Data Storage"
[10]: https://readmedium.com/csv-vs-parquet-vs-avro-choosing-the-right-tool-for-the-right-job-79c9f56914a8 "CSV vs Parquet vs Avro: Choosing the Right Tool for the Right Job"
[11]: https://www.upsolver.com/blog/the-file-format-fundamentals-of-big-data "Parquet, ORC, and Avro: The File Format Fundamentals of Big Data"
[12]: https://ghostinthedata.info/posts/2023/2023-02-12-choosing-the-right-file-format-for-big-data "Choosing the Right File Format for Big Data: A Comparison of Parquet ..."
[13]: https://stackoverflow.com/questions/71035663/why-avro-or-parquet-format-is-faster-than-csv "Why avro, or Parquet format is faster than csv? - Stack Overflow"
[14]: https://stackoverflow.com/questions/36822224/what-are-the-pros-and-cons-of-the-apache-parquet-format-compared-to-other-format "What are the pros and cons of the Apache Parquet format compared to ..."
[15]: https://geeklogbook.com/understanding-the-differences-between-parquet-avro-json-and-csv "Understanding the Differences Between Parquet, Avro, JSON, and CSV"
