# Large Model Strategies

Training large models requires careful management of memory, compute, and data.

## Techniques

- Model parallelism
  - Split model layers across GPUs when they cannot fit on a single device.

- ZeRO and optimizer sharding
  - Use DeepSpeed ZeRO stages to shard optimizer state, gradients, and parameters.

- Gradient checkpointing
  - Recompute intermediate activations during backpropagation to reduce memory usage at the cost of extra compute.

## Practical guidelines

- Start from established configurations for known architectures when possible.
- Validate that the data pipeline can feed GPUs efficiently before scaling up model size.
- Monitor memory and step time carefully during early runs.

These strategies enable the use of large models while controlling resource usage.
