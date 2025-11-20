# Cluster Architecture

The project uses a small set of standardized cluster configurations to simplify operations and cost management.

## Single-node GPU training cluster

Purpose:
- Fast prototyping and baseline training.

Characteristics:
- One driver node with 1 to 4 GPUs.
- Databricks Runtime for Machine Learning.
- Autotermination enabled for idle timeouts.
- Small to medium size CPU and memory to match GPU count.

## Distributed training cluster

Purpose:
- Large datasets or models that do not fit comfortably on a single node.

Characteristics:
- One driver node, multiple worker nodes, each with 1 or more GPUs.
- High-throughput network configuration.
- Databricks Runtime for Machine Learning with support for TorchDistributor and DeepSpeed.
- Cluster policy that enforces a maximum node count to control costs.

## Inference and batch scoring clusters

Purpose:
- Batch and streaming inference workloads when not using dedicated serving endpoints.

Characteristics:
- CPU or small GPU clusters depending on model size and latency requirements.
- Autoscaling enabled to handle bursts of workload.

Cluster policies capture the allowed instance families, autoscaling limits, and mandatory tags to ensure compliance and reproducibility.
