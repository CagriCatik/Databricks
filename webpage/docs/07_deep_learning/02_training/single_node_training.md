# Single Node Training

Single node GPU training is the primary path for rapid experimentation and baseline model development.

## Cluster configuration

- Databricks Runtime for Machine Learning.
- Single driver node with 1 to 4 GPUs.
- Moderate CPU and memory sized proportionally to GPU count.
- Autotermination enabled to control costs.

## Training workflow

1. Load curated data
   - Read from ml_silver.product_images_train as a Spark DataFrame.
   - Collect file paths and labels to the driver, or export a manifest.

2. Prepare PyTorch dataset
   - Implement a custom Dataset that loads images from file paths.
   - Apply augmentations such as random crops, flips, and normalization.

3. Define model
   - Use a pretrained backbone such as ResNet or EfficientNet.
   - Replace the final layer with a classifier for the project classes.

4. Train
   - Use an optimizer such as AdamW.
   - Implement early stopping based on validation loss.
   - Log metrics and artifacts with MLflow autologging.

The resulting model provides a strong baseline and a reference for later distributed training experiments.
