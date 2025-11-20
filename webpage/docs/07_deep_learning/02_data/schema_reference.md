# Schema Reference

This document provides example schemas for key Delta tables. Adapt column names and types to your specific domain.

## ml_bronze.product_images_raw

- file_path: string
- label_raw: string
- source_system: string
- ingestion_timestamp: timestamp
- extra_metadata: map<string, string>

## ml_silver.product_images_train

- file_path: string
- label_id: integer
- label_name: string
- split: string  // train, valid, test
- curated_timestamp: timestamp

## ml_gold.product_image_predictions (example inference table)

- prediction_id: string
- file_path: string
- label_id_pred: integer
- label_name_pred: string
- score: double
- scored_timestamp: timestamp
- model_version: string
- data_version: string

Keep schemas under version control and document breaking changes so that training and inference code can be updated safely.
