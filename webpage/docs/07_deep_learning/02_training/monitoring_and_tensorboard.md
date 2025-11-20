# Monitoring and TensorBoard

Monitoring ensures that training jobs behave as expected and provides visibility into model behavior.

## TensorBoard

- Training scripts write TensorBoard logs including loss curves, accuracy, and custom scalars.
- Databricks integrates with TensorBoard so that logs in DBFS can be visualized directly in the workspace.

## Cluster metrics

- GPU utilization, memory usage, CPU usage, and network throughput are monitored through Databricks cluster metrics.
- Spikes or underutilization can indicate issues with data loading, model size, or batch size.

## Logging practices

- Log key hyperparameters, learning rate schedules, and optimizer settings.
- Save sample predictions and failure cases as artifacts for offline inspection.
- Combine TensorBoard visualizations with MLflow metrics to gain a complete view of training behavior.

Effective monitoring shortens the feedback loop and reduces the risk of wasted compute due to misconfigured jobs.
