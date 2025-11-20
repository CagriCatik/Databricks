# Batch Inference

Batch inference scores large volumes of data in offline jobs, typically on a schedule.

## Workflow

1. Source data
   - Read unscored records from a Delta table or other source.
   - Filter to records that need scoring.

2. Load model
   - Use MLflow to load the Production model version as a pyfunc model or as a Spark UDF.

3. Score data
   - Apply the model as a Pandas UDF or pyfunc UDF to a Spark DataFrame.
   - Compute predictions and write them to a Delta table.

4. Post-processing
   - Join predictions back to business tables if needed.
   - Aggregate predictions for reporting or downstream analytics.

Batch inference is well suited to nightly scoring, periodic risk assessments, and large backfills of historical data.
