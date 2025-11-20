# Mosaic Streaming

Mosaic Streaming is used when data arrives continuously and you need low-latency ingestion into Delta tables.

## Use cases

- New items arriving from upstream systems in near real time.
- Log-like event streams that must be converted into training or inference data.

## Design

1. Define a streaming source
   - Read from cloud storage, Kafka, or another supported connector.
   - Apply schema inference or explicit schema definition.

2. Transform stream
   - Clean and normalize fields.
   - Enrich events with lookup tables for labels or metadata.

3. Write to Delta
   - Write to ml_bronze tables with trigger intervals configured based on latency needs.
   - Use checkpoint locations for exactly-once semantics where possible.

4. Downstream streaming views
   - Build streaming transformations from bronze to silver to keep curated training tables up to date.
   - Integrate with streaming inference jobs if online scoring is required.

Mosaic Streaming allows the same Delta tables to support both batch and streaming workflows with consistent semantics.
