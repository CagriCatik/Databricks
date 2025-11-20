# Synthetic Data Generation

Synthetic data supplements real data when labeled examples are scarce or imbalanced.

## Approaches

- Augmentation
  - Apply geometric and photometric transformations for images.
  - Use token-level or sequence-level transformations for text.

- Generative models
  - Use GANs, VAEs, or diffusion models to generate new samples.
  - Use language models to generate synthetic text examples.

- Programmatic labeling
  - Define labeling functions that assign labels based on rules or heuristics.

## Integration into training

- Validate that synthetic data improves performance on real validation sets.
- Limit the proportion of synthetic data if it diverges too far from real distributions.
- Track the use of synthetic data in MLflow runs for later analysis.

Synthetic data can significantly increase training signal when designed and validated carefully.
