# Optimization Best Practices

This document summarizes optimization guidelines for efficient and reliable deep learning training on Databricks.

## Batch size and learning rate

- Start with a batch size that fits comfortably in GPU memory.
- When increasing batch size, scale the learning rate approximately by the square root of the batch size factor.
- Observe loss curves and adjust as needed.

## Early stopping and scheduling

- Use early stopping based on validation loss or accuracy to avoid overfitting and wasted compute.
- Apply learning rate schedulers such as cosine decay or step decay to improve convergence.

## Transfer learning

- Prefer starting from pretrained models when domain appropriate.
- Fine-tune only higher layers first, then optionally unfreeze more layers.

## Data pipeline efficiency

- Avoid unnecessary data movement by reading directly from Delta where possible.
- Use binary data formats or TFRecord for record-based training when they show measurable benefit.

Applying these practices provides better performance and more predictable training behavior across different clusters and datasets.
