# Foundation Model Fine-tuning on Databricks

## Overview

Foundation Model Fine-tuning (part of Mosaic AI Model Training) enables customizing a foundation model with your own data to improve task-specific performance. It supports fine-tuning or continued training with significantly less data, time, and compute than training from scratch. The platform unifies data, training, tracking, governance, and deployment:

* Training data in your workspace.
* Foundation model selection.
* Checkpoints logged to MLflow.
* Model registered to Unity Catalog and deployable via Mosaic AI Model Serving.

Status: Public Preview in AWS regions us-east-1 and us-west-2.

## Capabilities

* Train with custom data; checkpoints saved to MLflow. You retain full control of the trained model.
* Auto-register trained models to Unity Catalog for serving.
* Continue training a previously fine-tuned proprietary model by loading its weights.
* Accessible via API or UI. See the tutorial on creating and deploying a Fine-tuning run.

## Supported Tasks

* Chat completion (recommended): Train on user-assistant chat logs; data is auto-formatted per model template.
* Instruction fine-tuning: Train on prompt-response pairs to adapt behavior, style, or instruction-following. No auto-formatting; use when custom formatting is required.
* Continued pre-training: Train on additional text to add knowledge or domain focus.

## Requirements

* Databricks workspace in us-east-1 or us-west-2.
* `pip install databricks_genai` for Fine-tuning APIs.
* Workspace must not use S3 access policies.
* Databricks Runtime 12.2 LTS ML or above if training data resides in Delta tables.
* Prepare input data as specified in the Fine-tuning data preparation guidance.

## Recommended Data Size and Training Duration

* Start with 1 to 4 epochs. After evaluation, continue training with 1 to 2 more epochs if outputs should hew closer to training data.
* If performance degrades on out-of-domain tasks or the model memorizes training data, reduce epochs.
* Instruction/chat tasks: Provide at least one full context length of tokens for the target model (for example, 131072 tokens for meta-llama/Llama-3.2-3B-Instruct).
* Continued pre-training: Minimum \~1.5M tokens recommended for higher quality adaptation.

## Supported Models

Maximum context length is 131072 for all listed models.

| Model                                  | Notes |
| -------------------------------------- | ----- |
| meta-llama/Llama-3.3-70B-Instruct      |       |
| meta-llama/Llama-3.2-1B                |       |
| meta-llama/Llama-3.2-1B-Instruct       |       |
| meta-llama/Llama-3.2-3B                |       |
| meta-llama/Llama-3.2-3B-Instruct       |       |
| meta-llama/Meta-Llama-3.1-70B          |       |
| meta-llama/Meta-Llama-3.1-70B-Instruct |       |
| meta-llama/Meta-Llama-3.1-8B           |       |
| meta-llama/Meta-Llama-3.1-8B-Instruct  |       |

Note: Supported models may change as new releases arrive and older models are deprecated.

## Model Licenses

* Meta Llama 3.2: Licensed under the LLAMA 3.2 Community License. Customers are responsible for compliance with the license and the Llama 3.2 Acceptable Use Policy.
* Meta Llama 3.1: Licensed under the LLAMA 3.1 Community License. Customers are responsible for compliance with applicable model licenses.

## Using the SDK (API)

Example: Create and launch a training run using data from Unity Catalog Volumes.

```python
from databricks.model_training import foundation_model as fm

model = "meta-llama/Meta-Llama-3.1-8B-Instruct"
# UC Volume with JSONL formatted data
train_data_path = "dbfs:/Volumes/main/mydirectory/ift/train.jsonl"
register_to = "main.mydirectory"

run = fm.create(
    model=model,
    train_data_path=train_data_path,
    register_to=register_to,
)
```

See the instruction fine-tuning NER demo for a full workflow covering data prep, run configuration, and deployment.

## Limitations

* Large datasets (10B+ tokens) are not supported due to compute availability.
* Continued pre-training workloads are limited to 60–256 MB files; files larger than 1 GB may incur longer processing times.
* Supported models may be updated or removed over time per the Generative AI models maintenance policy.
* AWS PrivateLink:

  * To use Fine-tuning with a PrivateLink enabled workspace, the workspace must be in us-west-2.
  * If storage also uses PrivateLink, Databricks recommends using Unity Catalog tables.
  * If storage firewalls protect Unity Catalog data, allowlist traffic from Databricks serverless data plane clusters. Contact your Databricks account team for details and potential custom solutions.

## When to Use Foundation Model Fine-tuning

* After trying few-shot learning and needing better quality.
* After prompt engineering on an existing model and needing improved results.
* When full ownership over a custom model is required for data privacy.
* When latency or cost constraints favor a smaller, task-specific model.

