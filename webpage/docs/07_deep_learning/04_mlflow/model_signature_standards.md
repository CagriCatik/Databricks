# Model Signature Standards

A clear model signature defines expected inputs and outputs and improves reliability across environments.

## Inputs

- Define input columns explicitly with names and types.
- For complex objects such as images, choose a representation such as base64-encoded strings or file paths with a stable schema.

## Outputs

- At minimum, outputs should include:
  - predicted_label or similar field.
  - score or probability associated with the prediction.
- Additional metadata such as model_version may be included when appropriate.

## Validation

- Use MLflow model signature tools or custom tests to validate that new model versions conform to the expected signature.
- Update clients only when necessary and document any signature changes.

Consistent signatures make it possible to swap model versions without breaking calling applications.
