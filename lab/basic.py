# Databricks notebook for basic data exploration

# COMMAND ----------

# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# COMMAND ----------

# Create Spark session
spark = SparkSession.builder.appName("SimpleNotebook").getOrCreate()

# COMMAND ----------

# Load a CSV file into Spark DataFrame
# Replace with your actual path
file_path = "/dbfs/tmp/sample_data.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)

# COMMAND ----------

# Show basic schema and first few rows
df.printSchema()
df.show(5)

# COMMAND ----------

# Basic summary statistics
df.describe().show()

# COMMAND ----------

# Filter data example
filtered_df = df.filter(col("some_column") > 100)
filtered_df.show(5)

# COMMAND ----------

# Convert Spark DataFrame to Pandas for plotting
pdf = df.toPandas()

# Plotting example
pdf["some_column"].hist(bins=30)
plt.title("Distribution of some_column")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()
