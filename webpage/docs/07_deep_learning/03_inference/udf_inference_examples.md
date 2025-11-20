# UDF Inference Examples

This document describes patterns for using models as UDFs in Spark DataFrames.

## Pyfunc UDF

- Use mlflow.pyfunc.spark_udf to create a UDF from a registered model.
- Apply the UDF to one or more columns of a DataFrame.

Example pattern:

- Load model as udf_model.
- df_scored = df.withColumn("prediction", udf_model("input_column")).

## Pandas UDF

- For vectorized inference, load the model in the UDF setup code and apply it to Pandas batches.
- This can provide better performance for large batch scoring.

## Practical tips

- Cache or broadcast configuration data used in the UDF to avoid repeated lookups.
- Prefer simple input schemas and serialize complex inputs such as images carefully.
- Measure performance and adjust partitioning, batch sizes, and cluster size as needed.

These UDF patterns allow reuse of the same registered model across batch, streaming, and exploratory workloads in notebooks.
