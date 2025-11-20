# Online Serving

Online serving uses Databricks Model Serving to provide low-latency predictions via REST endpoints.

## Setup

1. Select a Production model version in the registry.
2. Create a serving endpoint in Databricks bound to that model.
3. Configure scaling, request timeouts, and authentication.

## Request and response

- Requests typically contain the input features in JSON format, for example base64 encoded images or text.
- Responses contain predicted classes, scores, and optional metadata such as model version.

## Best practices

- Validate request payloads and return clear error messages for invalid inputs.
- Log request and response metadata where allowed for monitoring and debugging.
- Implement canary or blue-green deployments by directing a fraction of traffic to new model versions before full rollout.

Online serving provides the interface that external systems use to integrate machine learning predictions into real-time workflows.
