# LLM on Databricks

## Overview

Databricks provides multiple ways to access, integrate, and fine-tune **Large Language Models (LLMs)** for natural language processing (NLP) and generative AI applications.
Using Databricks Runtime for Machine Learning and built-in integrations, you can:

* Use open-source models like those from **Hugging Face**.
* Build and deploy **LangChain**-based LLM applications.
* Fine-tune **foundation models** with your own data.
* Access and experiment with models like **Azure OpenAI** and **OpenAI GPT** directly from SQL.

---

## Databricks Runtime for Machine Learning

* Preconfigured with popular LLM and NLP libraries:

  * **Hugging Face Transformers**
  * **LangChain**
  * **DSPy**
* Enables integration of pre-trained models or other open-source tools.
* Supports **fine-tuning** with your own data for improved domain-specific performance.
* GPU acceleration recommended for many LLM workloads.

---

## Foundation Model Fine-Tuning (Public Preview)

**Feature**: Part of **Mosaic AI Model Training**.

### Capabilities

* Fine-tune foundation models using **custom datasets**.
* Save **checkpoints to MLflow**.
* Retain **full control** of the fine-tuned model.
* Automatically **register models to Unity Catalog** for deployment with Model Serving.
* Fine-tune **existing proprietary models** by loading weights from previously fine-tuned versions.

**Workflow**:

1. Load base model.
2. Fine-tune on domain-specific dataset.
3. Save and register with **MLflow** and **Unity Catalog**.
4. Deploy with **Databricks Model Serving**.

---

## Hugging Face Transformers on Databricks

* **Library**: Preinstalled in **Databricks Runtime 10.4 LTS ML** and above.
* **Scaling**: Run NLP batch jobs or fine-tuning at scale on Databricks clusters.
* **Performance**: Best results often require **GPU hardware**; use CPU-optimized models when GPU is unavailable.
* **Use Cases**:

  * Text classification
  * Summarization
  * Translation
  * Question answering

**Example**: Fine-tuning a Hugging Face model on a single GPU is supported for targeted NLP applications.

---

## DSPy Integration

* **Purpose**: Automates prompt tuning by converting **natural language task descriptions** into:

  * Complete instructions
  * Few-shot examples
* **Use Case**: Reduce manual engineering of prompts for generative AI applications.
* See **Build generative AI apps using DSPy on Databricks** for implementation examples.

---

## LangChain on Databricks

* **Availability**: Experimental **MLflow flavor** (Databricks Runtime 13.1 ML and above).
* **Functionality**:

  * Build applications that integrate LLMs with external data sources.
  * Leverage **MLflow** tracking and deployment within Databricks.
* **Use Cases**:

  * Retrieval-augmented generation (RAG).
  * Knowledge-base powered LLMs.
  * Contextual question answering.

---

## AI Functions (Public Preview)

* **For SQL Users**:

  * Use Databricks Foundation Model APIs directly in SQL queries.
  * Access **external models** like **GPT-4 from OpenAI**.
  * Query **Mosaic AI Model Serving endpoints** from SQL.
* **Tasks Supported**:

  * Summarization
  * Content generation
  * Text classification
  * Data extraction

---

## Best Practices

* Use **GPU clusters** for large transformer-based model training or inference.
* Store models and checkpoints in **Unity Catalog** for governance and easy deployment.
* For streaming or large-scale inference, leverage **Databricks Model Serving** endpoints.
* For domain-specific tasks, fine-tune rather than relying solely on zero-shot performance.
* Use **LangChain** or **DSPy** for structured LLM workflows with improved context and accuracy.
