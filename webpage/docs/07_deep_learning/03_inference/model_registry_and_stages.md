# Model Registry and Stages

The MLflow Model Registry is the central catalog for models in this project.

## Concepts

- Registered model: a logical name, for example product_image_classifier.
- Model version: a specific instance of a model created from an MLflow run.
- Stages:
  - None: initial state for a new version.
  - Staging: candidates undergoing evaluation.
  - Production: models serving live or critical workloads.
  - Archived: retired versions kept for traceability.

## Workflow

1. Training logs a model to MLflow.
2. The model is registered under the chosen name.
3. A promotion process evaluates metrics and validation checks.
4. An approved version is transitioned to Staging and later to Production.
5. Downgrades or rollbacks are handled by transitioning stages between versions.

The registry provides a single source of truth for what is currently in production and how it was produced.
