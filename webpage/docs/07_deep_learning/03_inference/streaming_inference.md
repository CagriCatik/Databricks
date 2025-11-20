# Streaming Inference

Streaming inference applies models to data in motion, handling data as it arrives.

## Design

1. Define a structured streaming source
   - Read from a Delta table, Kafka, or other streaming connector.
   - Parse and validate incoming records.

2. Apply the model
   - Load the Production model from the registry.
   - Use a UDF to compute predictions within the streaming query.

3. Output results
   - Write predictions to a Delta sink or a message bus.
   - Maintain checkpoints to ensure fault tolerance.

## Considerations

- Latency: tune trigger intervals and batch sizes to meet latency targets.
- Throughput: scale clusters and optimize inference code to handle expected load.
- Monitoring: track lag, throughput, and error rates for the streaming query.

Streaming inference connects the model to real-time decision making systems with continuous updates.
