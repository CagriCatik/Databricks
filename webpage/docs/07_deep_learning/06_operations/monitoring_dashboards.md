# Monitoring Dashboards

Monitoring dashboards provide visibility into system and model behavior.

## Metrics to track

- Training
  - Job success rates and durations.
  - GPU utilization and cost.
  - Key training metrics such as loss and accuracy over time.

- Serving
  - Request volume and latency distributions.
  - Error rates and timeouts.
  - Model version currently in use.

- Data
  - Volume of ingested records.
  - Data quality check results.
  - Indicators of distributional shift.

## Implementation

- Use Databricks metrics and logs as primary data sources.
- Aggregate metrics into dashboards with filters for environment, model, and job type.
- Configure alerts on thresholds for critical metrics.

Dashboards help stakeholders understand the health of the deep learning system and react quickly to issues.
