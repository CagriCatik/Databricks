# Distributed Training with TorchDistributor

For larger datasets or models, training scales out to multiple GPUs and nodes using TorchDistributor and PyTorch DistributedDataParallel.

## Key concepts

- Each process corresponds to one GPU.
- DistributedDataParallel handles gradient synchronization.
- TorchDistributor launches training as a Spark job on worker nodes.

## Implementation outline

1. Wrap training in a main function
   - Initialize torch.distributed using environment variables.
   - Create a model and wrap it in DistributedDataParallel.
   - Use a DistributedSampler for the dataset.

2. Use TorchDistributor
   - In a Databricks notebook or job, create a TorchDistributor instance with num_processes set to the total GPU count.
   - Call the run method with the main training function and configuration parameters.

3. Logging
   - Use MLflow to record metrics, but limit logging to rank 0 to avoid duplication.
   - Optionally aggregate metrics across ranks before logging.

Distributed training with TorchDistributor minimizes changes to the training loop while unlocking multi-node scalability.
