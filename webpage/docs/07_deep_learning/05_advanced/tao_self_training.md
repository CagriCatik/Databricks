# TAO Style Self Training

Test-time adaptive optimization, or TAO-style self training, aims to improve models using synthetic or unlabeled data.

## Concept

- Use the current model to generate predictions on unlabeled or synthetic inputs.
- Define a reward or confidence signal for each prediction.
- Update the model based on this feedback, often using reinforcement learning techniques.

## Implementation outline

1. Data generation
   - Create synthetic variations of inputs using augmentation or generative models.
   - Collect unlabeled real-world samples when available.

2. Scoring and filtering
   - Run the current model to obtain predictions and confidence scores.
   - Filter samples based on confidence or other heuristics.

3. Optimization
   - Treat accepted samples as pseudo-labeled data.
   - Fine-tune the model periodically using this additional data.

This approach is experimental and should be introduced carefully with strong monitoring to avoid negative drift.
