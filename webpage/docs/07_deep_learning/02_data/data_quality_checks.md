# Data Quality Checks

Robust deep learning workflows depend on high quality data. This project includes a set of data quality checks for each layer.

## Bronze checks

- File existence: verify that referenced files exist in object storage.
- Basic schema validation: data types match expectations.
- Null ratio checks: label_raw and file_path should not be null.

## Silver checks

- Label integrity: label_id and label_name mappings are consistent.
- Split distribution: train, valid, and test splits meet target proportions.
- Class balance: per-class instance counts within acceptable range.

## Gold and inference checks

- Prediction completeness: all required fields such as model_version and data_version are populated.
- Drift indicators: track summary statistics of inputs and predictions over time.

Data quality checks can be implemented using simple PySpark assertions, Delta expectations, or external tools, and should be run as part of scheduled jobs.
