# Data Sources

This project is designed around a generic pattern for supervised learning, for example product image classification. You can adapt it to other domains.

Typical data sources:

1. Object storage
   - Image files or raw documents stored in cloud storage such as S3 or ADLS.
   - File paths and metadata captured in a manifest for ingestion.

2. Metadata systems
   - Product catalogs or label tables from operational databases.
   - Exported periodically as CSV, Parquet, or Delta tables.

3. Streaming sources
   - Event streams delivering new items or updates.
   - Integrated via Mosaic Streaming into Delta tables.

Each data source is ingested into Delta with an explicit bronze, silver, and optionally gold layer to separate raw, cleaned, and feature-ready data.
