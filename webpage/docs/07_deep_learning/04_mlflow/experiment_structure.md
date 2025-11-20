# MLflow Experiment Structure

Experiments in MLflow are organized to reflect different phases of the project and types of runs.

## Recommended experiments

- baseline_training
  - Single-node baseline models with stable configurations.

- distributed_training
  - Multi-GPU and multi-node runs.

- hyperparameter_tuning
  - Automated search trials with Optuna or Hyperopt.

- advanced_self_training
  - TAO-style or self-supervised runs.

## Run metadata

Each run should capture:

- Code version or Git commit hash.
- Data version or Delta table snapshot.
- Configuration file artifact.
- Cluster specification.

A consistent experiment structure makes it easier to compare runs and trace production models back to their origins.
