# E2E-RAG on Databricks


End-to-end reference implementation for building, evaluating, and deploying a Retrieval Augmented Generation (RAG) application on Databricks. The repository provides a sequential set of Markdown guides covering ingestion, preparation, embedding generation, vector search, model training, serving, and endpoint integration.

---

## Contents

### 1. Purpose

This project provides a complete guide for designing and delivering an LLM-based RAG system on Databricks. It covers architecture, data engineering, vector indexing, LLM usage, MLflow integration, model serving, and external endpoint consumption.

### 2. Objectives

- Present a production-grade architecture for LLM applications on Databricks.
- Show ingestion and preparation of data using Delta Lake and Unity Catalog.
- Demonstrate embedding generation and management.
- Configure and query Databricks Vector Search.
- Train, log, and register models using MLflow.
- Deploy RAG and LLM components with Databricks Model Serving.
- Integrate the final endpoint with external systems such as Microsoft Teams.

---

## Repository structure

- [Overview:](00_overview.md)
  - High-level problem statement, scope, and the end-to-end flow of the solution.

- [Architecture](01_architecture.md)
  - System architecture, core components, and data flow diagrams for the LLM solution on Databricks.

- [Data Ingestion](02_data_ingestion.md)
  - Data sources, ingestion strategies, and pipelines for loading raw data into Databricks Bronze or raw Delta tables.

- [Embeddings on Databricks](03_embeddings_on_databricks.md)
  - Methods for generating and managing text embeddings on Databricks, including model choices and embedding storage patterns.

- [Delta Table and Unity Catalog](04_delta_table_and_unity_catalog.md)
  - Organizing data in Delta tables, registering them in Unity Catalog, and managing access control and governance.

- [Databricks Vector Search](05_databricks_vector_search.md)
  - Setup and use of Databricks vector search for similarity retrieval over embeddings.

- [LLM on Databricks](06_llm_on_databricks.md)
  - Selecting, configuring, and executing LLMs on Databricks, including foundation models and fine-tuning approaches.

- [MLflow Integration](07_mlflow_integration.md)
  - MLflow experiment tracking, model registry usage, and governance for embedding and LLM models.

- [Model Serving](08_model_serving.md)
  - Deploying models via Databricks Model Serving with scaling, performance, and monitoring considerations.

- [Evaluation and Feedback](09_evaluation_and_feedback.md)
  - Methods for evaluating LLM output quality, RAG retrieval accuracy, and incorporating structured feedback loops.

- [Complete Databricks](10_complete_databricks.md)
  - Comprehensive walkthrough combining all previous modules into a single Databricks implementation pattern.

- [Teams Integration](11_teams_integration.md)
  - Integration patterns for connecting the Databricks LLM endpoint to Microsoft Teams through bots, message extensions, or webhooks.

- [Endpoint Implementation](12_endpoint-implementation.md)
  - Final endpoint implementation including request-response format, authentication, and operational best practices.

---

## Prerequisites

The material assumes familiarity with:

- Databricks (workspaces, clusters or SQL warehouses, Delta tables).
- Unity Catalog concepts (catalogs, schemas, permissions).
- MLflow for experiment tracking and model registry.
- Basic understanding of LLMs, embeddings, and RAG-style retrieval.
- Optional: Microsoft Teams or similar client platform for integration.

## Source

- [Build Your Chatbot Assistant With Databricks AI](https://app.getreprise.com/launch/dyRaj2X/)
- [Agentic Systems: Deploy and Evaluate RAG Apps with Databricks AI](https://www.databricks.com/resources/demos/tutorials/data-science/ai-agent?itm_data=demo_center)


---

# Documentation: Build Your Chatbot Assistant With Databricks AI

This screenshot shows the introductory overlay presented in the Databricks Catalog Explorer when accessing the demo volume `main.rag_chatbot.volume_databricks_documentation`. The overlay introduces a guided workflow for deploying a chatbot assistant using Databricks AI.

## Purpose of the Demo

The demo provides an end-to-end workflow for constructing a Retrieval Augmented Generation (RAG) application on Databricks. It explains how to ingest documents, build a vector index, and use Databricks models to generate responses enriched with retrieved context.

## Key Concepts Displayed

### RAG-based Chatbot Construction

The interface explains that the assistant uses Retrieval Augmented Generation. RAG combines:

- Document ingestion and parsing.
- Embedding generation and vector storage.
- Retrieval of semantically relevant content.
- Prompt construction augmented with retrieved data.
- Final answer generation using a Databricks-hosted model.

### Workflow Outline

The demo highlights the following sequence:

1. Load PDF documents into a Databricks volume as a knowledge base.
2. Parse the documents and build vector embeddings for retrieval.
3. Send user prompts enriched with retrieved context to a Databricks LLM endpoint (Llama 2 in this demo).
4. Produce grounded answers based on the combined prompt and retrieved document fragments.

### Demo Availability

The overlay states that the content can be installed directly into the user workspace. Two primary actions are provided:

- Download The Demo
- Get Started

These actions allow the user to either fetch the demo package or begin running it inside the Databricks environment.

## Context in UI

The screenshot shows the Catalog Explorer panel on the left, with the volume `volume_databricks_documentation` selected. This volume is used to store the knowledge base documents consumed by the RAG pipeline. The overlay explains the purpose of this volume and how it fits into the overall application flow.

The interface elements are part of Databricks Unity Catalog, ensuring controlled access, versioning, and management of the demo assets.

This page acts as the entry point for learning how to deploy and evaluate a RAG-based agentic system using Databricks AI.


![alt text](./images/image-0.png)

---

# Documentation: Navigating the Pre-Created Volumes for the RAG Chatbot

This screenshot shows the Catalog Explorer in Databricks after the user selects the Unity Catalog schema `rag_chatbot`. A guidance tooltip appears, instructing the user to explore the pre-created volume used in the RAG application workflow.

## Purpose of This Step

The tutorial is directing the user to open and inspect the dedicated Databricks Volume associated with the RAG chatbot demo. This volume acts as the storage location for all input documents used during ingestion, parsing, indexing, and retrieval.

The volume in focus is:

`main.rag_chatbot.volume_databricks_documentation`

This is a managed storage space created explicitly for the demo to hold PDF documents or other unstructured files that will serve as the knowledge base for the RAG pipeline.

## What the Interface Shows

The Catalog Explorer displays:

- The catalog: `rag_chat`
- The schema: `rag_chatbot`
- The volume: `volume_databricks_documentation` under the *Volumes* section
- Volume contents: currently empty, indicated by "No content in volume"
- Controls: an option to upload files directly into the volume via the button `Upload to this volume`

The guidance message indicates that the volume was automatically generated as part of the demo setup to streamline file upload and downstream processing.

## Role of the Volume in the RAG Workflow

A Databricks Volume provides governed, workspace-accessible storage under Unity Catalog. In this RAG application, the volume functions as:

- A landing zone for user-provided documents such as manuals, PDFs, or knowledge artifacts.
- The source of raw content to be parsed and converted into vector embeddings.
- A reproducible, governed document repository ensuring consistent ingestion during experimentation or deployment.

Once files are uploaded into this volume, subsequent steps in the demo will convert them into a searchable vector index used by the chatbot assistant.

This step ensures the user understands where document ingestion begins and how Databricks manages unstructured data in a RAG-driven agentic system.


![alt text](./images/image-1.png)


---

# Documentation: Uploading PDF Knowledge Sources Into the Databricks Volume

This screenshot shows the next guided step within the Databricks Catalog Explorer, instructing the user to upload PDF documents into the pre-created volume used for the RAG chatbot workflow.

## Purpose of This Step

The RAG pipeline requires a knowledge base consisting of unstructured documents. These documents are ingested, parsed, chunked, embedded, and indexed so that the chatbot can retrieve relevant context during prompting. The tutorial now directs the user to populate the storage volume with PDF files that will serve as the content foundation for the assistant.

## Interface Elements Highlighted

A tooltip appears near the top-right corner of the screen, pointing at the button:

**Upload to this volume**

The tooltip message states:

"Let's upload a few PDFs containing information on Databricks to our volume."

This instruction signals the user to begin the ingestion workflow by adding raw documents to the storage layer.

The main panel still shows:

- The volume: `main.rag_chatbot.volume_databricks_documentation`
- Current state: empty (no content in volume)

## Role of PDF Upload in the RAG Pipeline

Uploading documents into the volume initiates the knowledge ingestion process. These documents will be consumed by downstream pipeline components, which perform:

- Text extraction from PDFs
- Content preprocessing and segmentation into retrievable chunks
- Embedding computation using Databricks vectorization tools
- Storage of embeddings in a vector index for retrieval

The retrieval step is essential for ensuring that the LLM responds with grounded, document-supported answers rather than relying on model speculation.

## Workflow Context

This step transitions from environment overview to the beginning of practical data handling. At this stage, the user is expected to:

1. Gather relevant knowledge sources (PDF manuals, guides, documentation).
2. Upload them into the governed Unity Catalog Volume.
3. Prepare for the RAG-specific parsing and embedding steps that will follow.

By placing the files here, Databricks ensures controlled access, auditability, and reproducibility of the document ingestion process within the RAG application workflow.

This screenshot marks the first active data-ingestion action in the Agentic Systems: Deploy and Evaluate RAG Apps with Databricks AI tutorial.

![alt text](./images/image-2.png)

---

# Documentation: Uploading Multiple PDF Documents Into the RAG Chatbot Volume

This screenshot captures the file-upload dialog in Databricks after the user selects the option to upload documents into the Unity Catalog Volume `main.rag_chatbot.volume_databricks_documentation`. At this stage, multiple PDFs containing Databricks-related content are prepared for ingestion.

## Purpose of This Step

The RAG chatbot requires a substantial document repository to act as its knowledge base. By uploading Databricks e-books, reports, and technical guides, the user is populating the dataset that the assistant will rely on for retrieval and context augmentation.

These documents form the foundation upon which the retrieval augmented generation workflow operates. Every PDF is parsed, chunked, embedded, stored in a vector index, and later used to ground the model's responses with authoritative information.

## Interface Details

The upload dialog shows:

- Target path in the volume:
  `/Volumes/main/rag_chatbot/volume_databricks_documentation/databricks-pdf`
- Preview of files ready to upload (21 PDFs listed)
- A drag-drop upload zone
- An option to overwrite existing files with the same name
- A confirmation button labeled **Upload**

Next to the dialog, a contextual guidance bubble explains:

"We just uploaded dozens of files from our system.
These PDFs contain information and documentation related to Databricks.
Our goal is to create a chatbot that uses these documents as a knowledge source to provide more personalized answers to our customers."

This message clarifies the strategic purpose of the document ingestion step.

## Function of These Documents in the RAG Pipeline

Uploading documents initiates the creation of a structured, searchable knowledge layer. Once ingested, the workflow will:

- Extract text from each PDF
- Normalize and segment content into manageable chunks
- Generate vector embeddings for semantic search
- Store embeddings in a vector index governed by Unity Catalog
- Enable retrieval of context that will be included in prompts to the LLM

This prepares the system for accurate, grounded, and context-rich responses aligned with Databricks documentation.

## Workflow Positioning

This screenshot represents the transition from environment setup to content ingestion. After uploading:

1. The documents will appear in the volume directory.
2. Subsequent pipeline steps will transform raw documents into retrievable knowledge units.
3. The RAG-aware chatbot will be built using these enriched assets.

This completes the document upload portion of the Agentic Systems RAG application setup.

---
![alt text](./images/image-3.png)
---
![alt text](./images/image-4.png)
---
![alt text](./images/image-5.png)
---
![alt text](./images/image-6.png)
---
![alt text](./images/image-7.png)
---
![alt text](./images/image-8.png)
---
![alt text](./images/image-9.png)
---
![alt text](./images/image-10.png)
---
![alt text](./images/image-11.png)
---
![alt text](./images/image-12.png)
---
![alt text](./images/image-13.png)
---
![alt text](./images/image-14.png)
---
![alt text](./images/image-15.png)
---
![alt text](./images/image-16.png)
---
![alt text](./images/image-17.png)
---
![alt text](./images/image-18.png)
---
![alt text](./images/image-19.png)
---
![alt text](./images/image-20.png)
---
![alt text](./images/image-21.png)
---
![alt text](./images/image-22.png)
---
![alt text](./images/image-23.png)
---
![alt text](./images/image-24.png)
---
![alt text](./images/image-25.png)
---
![alt text](./images/image-26.png)
---
![alt text](./images/image-27.png)
---
![alt text](./images/image-28.png)
---
![alt text](./images/image-29.png)
---
![alt text](./images/image-30.png)
---
![alt text](./images/image-31.png)
---
![alt text](./images/image-32.png)
---
![alt text](./images/image-33.png)
---
![alt text](./images/image-34.png)
---
![alt text](./images/image-35.png)
---
![alt text](./images/image-36.png)
---
![alt text](./images/image-37.png)
---
![alt text](./images/image-38.png)
---
![alt text](./images/image-39.png)
---
![alt text](./images/image-40.png)
---
![alt text](./images/image-41.png)
---
![alt text](./images/image-42.png)
---
![alt text](./images/image-43.png)
---
![alt text](./images/image-44.png)
---
![alt text](./images/image-45.png)
---
![alt text](./images/image-46.png)
---
![alt text](./images/image-47.png)
---
![alt text](./images/image-48.png)
---
![alt text](./images/image-49.png)
---
![alt text](./images/image-50.png)
---
![alt text](./images/image-51.png)
---
![alt text](./images/image-52.png)
---
![alt text](./images/image-53.png)
---
![alt text](./images/image-54.png)
---
![alt text](./images/image-55.png)
---
![alt text](./images/image-56.png)