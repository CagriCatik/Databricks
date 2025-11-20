# Ray and Mosaic Composer

Ray and Mosaic Composer provide higher-level orchestration for distributed workloads that go beyond standard data parallel training.

## Ray integration

- Ray enables distributed hyperparameter searches, model ensembles, and complex workflows.
- Typical usage includes:
  - Launching parallel training trials with different hyperparameters or data subsets.
  - Coordinating reinforcement learning or self-play workloads.

## Mosaic Composer

- Mosaic Composer helps configure and manage complex distributed training setups.
- It can coordinate multiple distributed components, such as data loading, training, and evaluation stages.

## When to use

- When you need workflow-level parallelism in addition to model-level parallelism.
- When experiments involve multiple coordinated jobs, for example large-scale hyperparameter sweeps or multi-model pipelines.

Both Ray and Mosaic Composer complement TorchDistributor and DeepSpeed by focusing on orchestration and coordination rather than low-level gradient synchronization.
