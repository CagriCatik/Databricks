# System Overview

This project implements an end-to-end deep learning workflow on Databricks with the following major components:

1. Data layer
   - Raw data lands in cloud object storage.
   - Ingestion pipelines write raw and curated data as Delta Lake tables.
   - Optional Mosaic Streaming is used when data arrives continuously.

2. Training layer
   - Single-node GPU training using PyTorch and Databricks Runtime for Machine Learning.
   - Distributed training using TorchDistributor and, for large models, DeepSpeed Distributor.
   - Ray and Mosaic Composer are used for more complex distributed patterns when needed.

3. Experiment tracking and governance
   - MLflow is used to track experiments, metrics, artifacts, and model versions.
   - The MLflow Model Registry holds all promoted models with lifecycle stages.

4. Serving and inference
   - Online inference is provided via Databricks Model Serving REST endpoints.
   - Batch and streaming inference are implemented as Spark jobs using registered models.

5. Operations and monitoring
   - GPU cluster policies standardize resource usage.
   - TensorBoard and Databricks metrics monitor training.
   - Dashboards track model and endpoint health.

All components are designed to be modular, so you can replace or extend pieces, for example swapping PyTorch for TensorFlow or adding additional data sources.
