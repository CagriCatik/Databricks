# Distributed Training with DeepSpeed Distributor

DeepSpeed Distributor is used when model size or batch size requires more efficient memory handling than standard DataParallel or DDP.

## When to use

- Very large models that approach or exceed single GPU memory capacity.
- Scenarios that benefit from ZeRO optimizations or gradient checkpointing.

## Configuration

1. DeepSpeed config file
   - Define optimizer, learning rate schedule, and ZeRO optimization stage.
   - Configure gradient accumulation and checkpointing parameters.

2. Training entry point
   - Initialize DeepSpeed in the training script, wrapping the model and optimizer.
   - Adjust the training loop to use DeepSpeed engine methods for forward, backward, and step.

3. Launch via DeepSpeed Distributor
   - Use Databricks DeepSpeed Distributor to distribute the training entry point across GPUs.
   - Ensure that environment variables and cluster networking support the chosen DeepSpeed backend.

DeepSpeed allows you to push model and batch sizes beyond what would be possible with standard data parallel training, while still integrating with MLflow and the Databricks environment.
