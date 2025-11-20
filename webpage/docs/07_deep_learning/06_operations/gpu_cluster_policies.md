# GPU Cluster Policies

Cluster policies standardize how GPU resources are used and help control cost and risk.

## Policy elements

- Allowed instance families and GPU types.
- Maximum number of nodes and GPUs per cluster.
- Required tags for cost allocation and ownership.
- Idle autotermination timeouts.

## Policy types

- Development clusters
  - Smaller size, shorter timeouts.
  - Intended for interactive exploration.

- Training clusters
  - Larger size, stricter controls.
  - Used by scheduled jobs and high priority training runs.

Clear cluster policies prevent resource misuse and help ensure that critical workloads have enough capacity.
