# Delta Lake Layout

The Delta Lake layout follows a multi-layered structure to enforce data quality and simplify downstream usage.

## Bronze layer

- Tables store raw ingested data with minimal transformation.
- Example:
  - ml_bronze.product_images_raw
- Columns might include:
  - file_path, label_raw, ingestion_timestamp, source_system

## Silver layer

- Tables store cleaned and standardized data.
- Example:
  - ml_silver.product_images_train
- Transformations include:
  - Cleaned labels and standardized label IDs.
  - Removal of corrupted or missing records.
  - Balanced train, validation, and test splits encoded as a split column.

## Gold layer (optional)

- Feature-ready views for specific models or use cases.
- Example:
  - ml_gold.product_image_features
- May include precomputed features or embeddings.

All tables use Delta Lake to provide ACID transactions, schema enforcement, time travel, and efficient reads for training and inference.
