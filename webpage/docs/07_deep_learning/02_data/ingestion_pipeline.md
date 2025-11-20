# Ingestion Pipeline

The ingestion pipeline moves data from raw sources into Delta tables suitable for training.

## Steps

1. Discover new data
   - A job scans the object storage bucket or receives notifications of new files.
   - New file paths are added to a staging DataFrame.

2. Load metadata and labels
   - Join file paths with label tables from upstream systems.
   - Apply basic validation such as checking that labels are not null.

3. Write to bronze Delta
   - Write the combined DataFrame to ml_bronze.product_images_raw in append mode.
   - Preserve ingestion timestamps and source identifiers.

4. Curate into silver Delta
   - Read ml_bronze.product_images_raw.
   - Filter duplicates or invalid records.
   - Normalize labels and compute split assignments.
   - Write to ml_silver.product_images_train using overwrite or merge semantics.

5. Optional streaming
   - If data arrives continuously, implement steps 1 to 4 as a streaming query using Mosaic Streaming.

The ingestion notebooks and jobs are parameterized by source paths and table names to support multiple datasets and environments.
