# Autologging Behavior

MLflow autologging simplifies the capture of training details but should be understood clearly.

## What is logged

- Parameters: learning rate, batch size, number of epochs, and others inferred from the framework.
- Metrics: training and validation loss, accuracy, and other standard metrics.
- Artifacts: model weights, TensorBoard logs, and configuration files when configured.

## Framework specifics

- For PyTorch, mlflow.pytorch.autolog integrates with the training loop to log models and metrics when the training completes.
- Custom logging can be added alongside autologging to record domain-specific metrics or artifacts.

## Limitations and guidelines

- Avoid logging large raw datasets as artifacts; instead, log references to Delta tables.
- Ensure that sensitive data is not included in logged artifacts or parameters.
- Review logged information periodically to confirm it matches project expectations.

Proper use of autologging reduces boilerplate while preserving full observability of training runs.
