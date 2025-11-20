# Component Interactions

This document explains how the main components of the system interact in a typical training and deployment lifecycle.

## Data to training

1. Ingestion jobs read raw data from object storage and write Delta tables in bronze and silver layers.
2. Training notebooks read curated Delta tables from the silver layer using Spark.
3. Spark DataFrames are converted into formats suitable for training:
   - File path lists for PyTorch Dataset implementations.
   - Serialized record formats such as TFRecord when beneficial.

## Training to MLflow

1. Training scripts use MLflow autologging to capture parameters, metrics, and artifacts.
2. Each experiment run is associated with a specific data snapshot version in Delta.
3. The best performing model from an experiment is registered into the MLflow Model Registry.

## Registry to serving

1. A selected model version in the registry is transitioned to the Staging or Production stage.
2. Databricks Model Serving is configured to serve the Production version of the model.
3. External clients call the REST endpoint for online predictions.

## Inference feedback loop

1. Batch and streaming inference jobs score new data using the production model.
2. Predictions and outcomes are written back to Delta tables.
3. These tables can be analyzed for drift and used to trigger retraining jobs.

This interaction pattern ensures traceability from input data through training and deployment to downstream usage.
