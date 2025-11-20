# Job Orchestration

Job orchestration coordinates the various notebooks and scripts in the project.

## Tools

- Databricks Jobs for scheduled and triggered runs.
- Job tasks referencing notebooks or Python scripts in the repository.
- Optional integration with external orchestrators such as Airflow.

## Example flow

1. Ingestion jobs populate bronze and silver Delta tables.
2. Training jobs run daily or on demand, reading the latest curated data.
3. Evaluation jobs assess new models and update registry stages if criteria are met.
4. Inference jobs score new data or refresh predictions.

Failures should be logged and surfaced through alerting channels for rapid intervention.
