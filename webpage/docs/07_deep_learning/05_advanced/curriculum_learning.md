# Curriculum Learning

Curriculum learning trains models on easier examples first and gradually introduces harder ones.

## Motivation

- Stabilize training and improve convergence.
- Encourage the model to learn basic patterns before complex ones.

## Design

1. Difficulty scoring
   - Define a difficulty measure based on heuristics, model confidence, or external labels.
   - Partition the dataset into difficulty bands.

2. Training schedule
   - Start training on the easiest band.
   - Gradually mix in more difficult bands according to a schedule.

3. Evaluation
   - Monitor performance on held-out validation data across all difficulty levels.
   - Adjust the curriculum if learning plateaus or regresses.

Curriculum learning can be combined with standard training pipelines without significant architectural changes.
