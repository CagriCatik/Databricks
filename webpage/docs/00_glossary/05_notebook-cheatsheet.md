# Databricks Python Notebook Cheatsheet

This focuses on using Python inside Databricks notebooks: notebook basics, magic commands, Spark, data I/O, plotting, and utilities.

## 1. Cell basics

Run current cell:

* Ctrl + Enter

Run and go to next:

* Shift + Enter

Change cell language (first line):

* `# Databricks notebook source` is auto-added in exports.
* Use a language magic at top:

  * `%python`
  * `%sql`
  * `%scala`
  * `%r`

Comments:

```python
# single line
"""
multi
line
comment
"""
```

## 2. Common magic commands

Language selection per cell:

```python
%python
%sql
%scala
%r
```

Install Python packages (cluster or notebook scoped, depending on config):

```python
%pip install requests
%pip install "pandas==2.2.0"
```

Run another notebook:

```python
%run /Shared/utils   # path in workspace
```

Execute shell commands:

```python
%sh ls
%sh pip list
```

Switch to SQL temporarily:

```python
%sql
SELECT 1;
```

Display environment info (when available):

```python
%fs ls /          # Files in DBFS
```



## 3. dbutils essentials



`dbutils` is Databricks utilities object (file system, secrets, widgets, etc.).

Files (DBFS):

```python
dbutils.fs.ls("/")             # list
dbutils.fs.mkdirs("/tmp/data") # make dir
dbutils.fs.rm("/tmp/data", True)  # True = recursive
dbutils.fs.cp("/src/file.csv", "/dest/file.csv", True)
```

Text file helpers:

```python
dbutils.fs.put("/tmp/hello.txt", "Hello Databricks", overwrite=True)
data = dbutils.fs.head("/tmp/hello.txt", 1000)  # first bytes as string
```

Secrets (requires secret scope configured):

```python
token = dbutils.secrets.get(scope="my-scope", key="api-token")
```

Notebook workflows:

```python
# Call another notebook with parameters
result = dbutils.notebook.run(
    "/Shared/child_notebook",  # path
    timeout_seconds=600,
    arguments={"param1": "value1"}
)

dbutils.notebook.exit("Finished")  # return value to caller
```

Widgets (for parameters / UI controls):

```python
# Create
dbutils.widgets.text("my_text", "default", "Input label")
dbutils.widgets.dropdown("color", "red", ["red", "green", "blue"], "Color")
dbutils.widgets.multiselect("ids", "1", ["1","2","3"], "IDs")
dbutils.widgets.combobox("name", "Alice", ["Alice","Bob"], "Name")

# Get
value = dbutils.widgets.get("my_text")

# Remove
dbutils.widgets.remove("my_text")
dbutils.widgets.removeAll()
```

## 4. SparkSession and basic Spark usage

In Databricks Python notebooks, `spark` (SparkSession) is usually predefined.

Check Spark:

```python
spark
```

Create DataFrame:

```python
from pyspark.sql import Row
from pyspark.sql import functions as F

df = spark.createDataFrame(
    [
        (1, "Alice", 10.5),
        (2, "Bob",   20.0),
    ],
    ["id", "name", "score"]
)

df.show()
df.printSchema()
```

Read data:

```python
df = spark.read.parquet("/mnt/data/events")
df_csv = spark.read.option("header", True).csv("/mnt/data/file.csv")
df_json = spark.read.json("/mnt/data/logs.json")
```

Write data:

```python
df.write.mode("overwrite").parquet("/mnt/output/events")
df.write.mode("append").format("delta").save("/mnt/output/delta-table")
```

Transformations:

```python
df = df.filter(F.col("score") > 10)
df = df.withColumn("score2", F.col("score") * 2)
df_grouped = df.groupBy("name").agg(F.avg("score").alias("avg_score"))
df_ordered = df_grouped.orderBy(F.desc("avg_score"))
```

Create / use temp views (for SQL):

```python
df.createOrReplaceTempView("events")

# in Python cell
spark.sql("SELECT name, AVG(score) AS avg_score FROM events GROUP BY name").show()
```

## 5. Tables, SQL, and Delta

Create table from DataFrame:

```python
df.write.mode("overwrite").saveAsTable("analytics.events")
```

Read table:

```python
df = spark.table("analytics.events")
df = spark.read.table("analytics.events")
```

Basic SQL in `%sql` cell:

```sql
SELECT * FROM analytics.events LIMIT 10;

CREATE TABLE analytics.delta_events
USING DELTA
AS
SELECT * FROM analytics.events;
```

Delta Lake for versioned tables:

```python
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, "/mnt/output/delta-table")

# Time travel read
old_df = spark.read.format("delta").option("versionAsOf", 3).load("/mnt/output/delta-table")

# Update / delete
delta_table.update(
    condition="score < 0",
    set={"score": "0"}
)

delta_table.delete("score IS NULL")
```

## 6. Pandas + Spark interop

Spark -> Pandas:

```python
pdf = df.toPandas()
```

Pandas -> Spark:

```python
import pandas as pd

pdf = pd.DataFrame({"id": [1,2], "value": ["a", "b"]})
df = spark.createDataFrame(pdf)
```

Efficient from files:

```python
df = spark.read.parquet("/mnt/data")
```

## 7. Data access: DBFS, mount points, external

DBFS paths:

Logical path:

```python
"/mnt/data/file.parquet"    # recommended
"dbfs:/mnt/data/file.parquet"
```

Access from Spark:

```python
df = spark.read.parquet("/mnt/data/file.parquet")
```

Access from Python (local driver path):

```python
with open("/dbfs/mnt/data/file.parquet", "rb") as f:
    raw = f.read()
```

List files:

```python
dbutils.fs.ls("/mnt")
```

## 8. Plotting and display utilities

Basic display:

```python
display(df)        # Databricks built-in table / chart UI
displayHTML("<h1>Hello</h1>")
```

Matplotlib:

```python
import matplotlib.pyplot as plt

pdf = df.toPandas()

plt.figure()
pdf["score"].hist(bins=20)
display(plt.gcf())   # sometimes needed to show figure
```

## 9. MLflow quick reference (Databricks-native)

Start and log a run:

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("model_type", "random_forest")
    mlflow.log_metric("rmse", 0.123)
    mlflow.log_artifact("/dbfs/tmp/model_plot.png")
```

Autolog (for supported libraries, e.g., scikit-learn):

```python
import mlflow.sklearn
mlflow.sklearn.autolog()

with mlflow.start_run():
    model.fit(X_train, y_train)
```

Load model:

```python
model_uri = "runs:/<run_id>/model"
model = mlflow.sklearn.load_model(model_uri)
```

## 10. Notebook parameters pattern

Define widgets for parameters:

```python
dbutils.widgets.text("input_path", "/mnt/data/raw", "Input path")
dbutils.widgets.text("output_path", "/mnt/data/processed", "Output path")

input_path = dbutils.widgets.get("input_path")
output_path = dbutils.widgets.get("output_path")
```

Then run notebook from another notebook or job:

```python
result = dbutils.notebook.run(
    "/Shared/etl_job",
    timeout_seconds=3600,
    arguments={
        "input_path": "/mnt/source",
        "output_path": "/mnt/target"
    },
)
```

## 11. Performance tips (basic)

Repartition / coalesce:

```python
df = df.repartition(200, "key_column")  # increase partitions for large shuffles
df_small = df_small.coalesce(1)        # reduce partitions for small datasets
```

Cache DataFrame:

```python
df_cached = df.cache()
df_cached.count()   # materialize cache
```

Avoid `df.toPandas()` on large data; sample first:

```python
small_pdf = df.sample(fraction=0.01).toPandas()
```

## 12. Jobs and workflows hooks (from notebook)

Access job context (if running as a Job):

```python
task_context = dbutils.jobs.taskValues
# Example: get value set by another task
val = task_context.get(taskKey="upstream_task", key="some_key", default="NA")
```

Set task values:

```python
dbutils.jobs.taskValues.set(key="records_processed", value="12345")
```

## 13. Quick reference: typical ETL skeleton

```python
from pyspark.sql import functions as F

# 1. Parameters
dbutils.widgets.text("input_path", "/mnt/raw/events", "Input")
dbutils.widgets.text("output_path", "/mnt/curated/events", "Output")

input_path = dbutils.widgets.get("input_path")
output_path = dbutils.widgets.get("output_path")

# 2. Read
df = spark.read.parquet(input_path)

# 3. Transform
df_tr = (
    df
    .filter(F.col("event_type") == "click")
    .withColumn("event_date", F.to_date("event_time"))
    .groupBy("user_id", "event_date")
    .agg(F.count("*").alias("clicks"))
)

# 4. Write as Delta
(
    df_tr
    .write
    .format("delta")
    .mode("overwrite")
    .save(output_path)
)

# 5. Optionally create / refresh table
spark.sql(f"""
CREATE TABLE IF NOT EXISTS analytics.daily_clicks
USING DELTA
LOCATION '{output_path}'
""")
```

This covers the core operations you typically need in a Python-focused Databricks notebook: environment, utilities, Spark, Delta, parameters, visuals, and MLflow hooks.
