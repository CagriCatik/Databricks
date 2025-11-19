# End-to-End RAG on Databricks

Implementation-focused documentation

This describes how to build a full RAG system *only* with Databricks components:

* Unity Catalog (data, models, permissions)
* Delta tables
* Vector Search
* Mosaic AI models
* LangChain (Databricks integration)
* MLflow (tracking, registry, deployment)
* Model Serving and Eval Apps

I will assume you start from raw documents (PDFs, text, etc.) in cloud storage and want a production-grade RAG chatbot.

---

## 1. Architecture overview

Logical steps on Databricks:

1. Ingest raw documents into Databricks (Volumes or cloud storage paths).
2. Parse documents, extract text, chunk, and generate embeddings (in a notebook or jobs).
3. Store chunks + embeddings in a Delta table under Unity Catalog.
4. Build a Vector Search index on that Delta table.
5. Implement the RAG chain using:

   * Databricks Vector Search retriever
   * Mosaic AI-hosted LLM via Databricks model serving
   * LangChain chain logic
6. Use MLflow to:

   * Track runs and traces
   * Log the chain as a model
   * Register it in Unity Catalog
7. Serve the chain via Databricks Model Serving.
8. Use playground / eval apps to test and collect feedback.

Everything lives inside Databricks; no external preprocessing platform.

---

## 2. Data ingestion and preprocessing on Databricks

### 2.1 Where documents live

Typical options:

* Directly in cloud storage mounted / referenced by Databricks:

  * `s3://...`
  * `abfss://...`
  * `gs://...`
* Databricks Volumes (recommended now; managed storage under Unity Catalog).

Example: documents in a Volume:

```python
doc_dir = "/Volumes/company_docs/raw/sec_filings"
```

### 2.2 Parsing PDFs / documents

You need to:

* Read each document.
* Extract text and optionally metadata (page, section, title).

You can use Python libraries inside a Databricks notebook (run as a Job in production), e.g.:

* `pypdf` or `pdfplumber` for PDFs.
* `python-docx` for Word.
* Custom HTML parsers for web-like content.

Example for PDF-only (minimal):

```python
import os
from pypdf import PdfReader

def extract_pdf(doc_path):
    reader = PdfReader(doc_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append({"page": i + 1, "text": text})
    return pages
```

You then iterate over files in the directory:

```python
import glob

raw_docs = []

for path in glob.glob(os.path.join(doc_dir, "*.pdf")):
    file_name = os.path.basename(path)
    pages = extract_pdf(path)
    for p in pages:
        raw_docs.append(
            {
                "file_name": file_name,
                "page": p["page"],
                "text": p["text"],
            }
        )
```

You can convert this to a Spark DataFrame and write to a staging Delta table.

```python
df_raw = spark.createDataFrame(raw_docs)
df_raw.write.format("delta").mode("overwrite").saveAsTable(
    "catalog.schema.docs_raw"
)
```

This is the simplest variant. In a real system you probably:

* Normalize encodings.
* Remove boilerplate.
* Extract structured sections and headings.
* Add custom metadata (document type, customer, region, etc.).

### 2.3 Chunking

RAG works better on semantically meaningful chunks. A basic chunker:

* Splits text by max length.
* Tries to respect sentence boundaries.

Example chunking function:

```python
import re
from typing import List

def split_into_sentences(text: str) -> List[str]:
    # Very naive splitter; replace with something robust if needed.
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in sentences if s]

def chunk_text(text: str, max_chars: int = 1000, overlap: int = 200) -> List[str]:
    sentences = split_into_sentences(text)
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) + 1 <= max_chars:
            current = (current + " " + s).strip()
        else:
            if current:
                chunks.append(current)
            # start new chunk with overlap
            if overlap > 0 and chunks:
                # use tail of previous chunk as overlap 
                tail = chunks[-1][-overlap:]
                current = tail + " " + s
            else:
                current = s
    if current:
        chunks.append(current)
    return chunks
```

Use it in Spark UDF or mapInPandas to produce chunk rows:

```python
from pyspark.sql.functions import col, explode, pandas_udf
import pandas as pd

@pandas_udf("file_name string, page int, chunk_id int, chunk_text string")
def make_chunks(batch: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in batch.iterrows():
        chunks = chunk_text(row["text"], max_chars=1000, overlap=200)
        for i, ch in enumerate(chunks):
            rows.append(
                {
                    "file_name": row["file_name"],
                    "page": int(row["page"]),
                    "chunk_id": i,
                    "chunk_text": ch,
                }
            )
    return pd.DataFrame(rows)

df_chunks = (
    spark.table("catalog.schema.docs_raw")
    .groupBy("file_name", "page")
    .apply(make_chunks)
)

df_chunks.write.format("delta").mode("overwrite").saveAsTable(
    "catalog.schema.docs_chunks"
)
```

Now you have a table of chunks.

---

## 3. Embeddings on Databricks

Use Mosaic AI or a hosted embedding model via Databricks Model Serving.

### 3.1 Embedding endpoint

You host an embedding model as a Databricks serving endpoint (e.g. `text-embedding-3-small` or a local embedding model). [Speculation] Exact name depends on your environment.

Assume endpoint:

* `embeddings-finance-endpoint`

Example: call it from a notebook / job:

```python
import requests
import json
import os

DATABRICKS_HOST = os.environ["DATABRICKS_HOST"]
DATABRICKS_TOKEN = os.environ["DATABRICKS_TOKEN"]
ENDPOINT_NAME = "embeddings-finance-endpoint"

def embed_batch(texts):
    url = f"{DATABRICKS_HOST}/serving-endpoints/{ENDPOINT_NAME}/invocations"
    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"inputs": texts}
    resp = requests.post(url, headers=headers, data=json.dumps(payload))
    resp.raise_for_status()
    return resp.json()["embeddings"]
```

Implementation details depend on the serving endpoint contract. [Unverified]

### 3.2 Embedding chunks table

You embed the `chunk_text` column and store the result as a vector column in the same Delta table.

Pattern:

```python
from pyspark.sql.functions import collect_list, struct, col
from pyspark.sql.types import ArrayType, FloatType

# Simple non-UDF approach: collect to driver in manageable batches.
df = spark.table("catalog.schema.docs_chunks")

# In production: do this in streaming or in partitions to avoid driver overload.
chunks = df.select("file_name", "page", "chunk_id", "chunk_text").collect()

embedded_rows = []
batch_size = 64

for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i + batch_size]
    texts = [r["chunk_text"] for r in batch]
    vectors = embed_batch(texts)
    for r, vec in zip(batch, vectors):
        embedded_rows.append(
            (
                r["file_name"],
                r["page"],
                r["chunk_id"],
                r["chunk_text"],
                vec,
            )
        )

schema = "file_name string, page int, chunk_id int, chunk_text string, embedding array<float>"
df_emb = spark.createDataFrame(embedded_rows, schema=schema)

df_emb.write.format("delta").mode("overwrite").saveAsTable(
    "catalog.schema.docs_chunks_embedded"
)
```

For large-scale, you want a UDF with a vector-return type and call the endpoint per partition, or use a native Databricks embedding function if available in your workspace.

---

## 4. Delta table and Unity Catalog

You now have:

* `catalog.schema.docs_chunks_embedded`

Columns:

* `file_name` (string)
* `page` (int)
* `chunk_id` (int)
* `chunk_text` (string)
* `embedding` (array<float>)

Configure privileges in Unity Catalog:

* `GRANT SELECT ON TABLE catalog.schema.docs_chunks_embedded TO <group/role>`.

Unity Catalog is the single governance layer for:

* Tables (your chunks).
* Vector search indexes.
* Models.

---

## 5. Databricks Vector Search

### 5.1 Create index from UI

From Data explorer:

1. Open `catalog.schema.docs_chunks_embedded`.
2. Click "Create vector search index".
3. Configure:

   * Endpoint name: e.g. `vs-finance-endpoint`.
   * Index name: e.g. `catalog.schema.vs_finance_10k`.
   * Primary key: you can create a composite ID, or add a new `id` column.
   * Embedding column: `embedding`.
   * Embedding dimension: must match your model.
   * Sync config: auto or triggered.

If you do not have a primary key column, add an `id` column:

```python
from pyspark.sql.functions import monotonically_increasing_id

df = spark.table("catalog.schema.docs_chunks_embedded")
df_with_id = df.withColumn("id", monotonically_increasing_id())
df_with_id.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(
    "catalog.schema.docs_chunks_embedded"
)
```

Then use `id` as PK in the index.

### 5.2 LangChain Vector Search retriever

Databricks provides a LangChain integration for Vector Search.

Pattern :

```python
from databricks.vector_search.langchain import DatabricksVectorSearch

retriever = DatabricksVectorSearch(
    endpoint_name="vs-finance-endpoint",
    index_name="catalog.schema.vs_finance_10k",
).as_retriever(
    search_kwargs={"k": 5}
)
```

Double-check exact class names in your environment. [Unverified]

---

## 6. LLM on Databricks (Mosaic AI)

Use a Databricks-hosted LLM via model serving (Mosaic AI), accessed through LangChain.

Assume you have a chat endpoint, e.g.:

* `llm-finance-llama-endpoint`

### 6.1 LangChain ChatDatabricks

Pattern:

```python
from langchain.chat_models import ChatDatabricks
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableMap, RunnablePassthrough

system_template = """
You are a helpful assistant that answers questions about financial documents.
You must only use the given context. If information is missing, say you do not know.
Be concise and factual.
"""

human_template = """
Question:
{question}

Context:
{context}
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("human", human_template),
    ]
)

llm = ChatDatabricks(
    endpoint="llm-finance-llama-endpoint"
)
```

### 6.2 Assemble RAG chain

Helper for formatting docs:

```python
def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)
```

Full chain:

```python
rag_chain = (
    RunnableMap(
        {
            "question": RunnablePassthrough(),
            "context": retriever | format_docs,
        }
    )
    | prompt
    | llm
    | StrOutputParser()
)
```

Usage:

```python
question = "Describe the competitive landscape for Walmart."
answer = rag_chain.invoke(question)
print(answer)
```

This is essentially what was shown in the demo, but without any external preprocessing service.

---

## 7. MLflow integration

### 7.1 Traces and autologging

To inspect the behavior of the chain (retrieval, prompts, etc.), use MLflow integration for LangChain.

Pattern :

```python
import mlflow

mlflow.langchain.autolog()  # exact API name may differ [Unverified]

with mlflow.start_run():
    q = "What are the key risks highlighted in the latest 10-K for Walmart?"
    a = rag_chain.invoke(q)
    print(a)
```

In the MLflow UI, you will see:

* A run with:

  * Inputs (question).
  * Trace steps (retriever calls, LLM calls).
  * Retrieved documents metadata from your Delta table.

### 7.2 Log and register model

You want the RAG chain itself registered as a model in Unity Catalog.

Pattern:

```python
with mlflow.start_run() as run:
    sample_question = "Describe the competitive landscape for Walmart."
    _ = rag_chain.invoke(sample_question)

    mlflow.langchain.log_model(
        lc_model=rag_chain,
        artifact_path="model",
        registered_model_name="catalog.schema.rag_finance_assistant"
    )
```

This both logs the chain and registers it in Unity Catalog with name:

* `catalog.schema.rag_finance_assistant`

If your MLflow version does not support `mlflow.langchain.log_model`, you can wrap the chain in a PythonModel and log that.

---

## 8. Model Serving

Once the model is registered under Unity Catalog, you can deploy it as a serving endpoint.

Steps:

1. Go to Model Serving in Databricks.
2. Create Endpoint.
3. Select model: `catalog.schema.rag_finance_assistant`.
4. Choose model version.
5. Configure compute / scaling.
6. Deploy.

The endpoint accepts JSON input, typically with a `question` field. The RAG chain inside the model will:

* Call Vector Search.
* Construct prompts.
* Call the LLM.
* Return the final answer.

You can test it in the UI or via REST.

Example REST call (pattern, contract depends on model wrapper):

```bash
curl -X POST \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  https://<databricks_host>/serving-endpoints/rag-finance-assistant/invocations \
  -d '{"inputs": {"question": "Describe the competitive landscape for Walmart."}}'
```

---

## 9. Evaluation and feedback

Databricks provides evaluation apps (review apps) for hosted models.

### 9.1 Eval app from the model

From model or endpoint page:

1. Click "Create evaluation app" or similar.
2. Define:

   * Input schema (e.g. `question` string).
   * Output fields to display (e.g. `answer`, `references` if you add them).
   * Evaluation questions: accuracy, relevance, safety, usefulness.

Then you get a web UI where:

* Users type questions.
* The app calls your serving endpoint.
* Users label:

  * Is this accurate?
  * Is this relevant?
  * Is this safe/helpful?

The feedback is stored as an evaluation dataset.

You can then:

* Export this dataset.
* Use it for:

  * Prompt optimization.
  * Model selection.
  * Fine-tuning LLMs specific to your content.

---

## 10. Complete Databricks-only RAG checklist

Concrete steps without Unstructured:

1. **Store docs**

   * Put raw docs in Volumes or referenced cloud paths.
2. **Parse and normalize**

   * Use PDF/text/Word parsers in a Databricks job.
   * Write `docs_raw` Delta table (file, page, text, metadata).
3. **Chunk**

   * Implement chunking (sentence/paragraph-aware).
   * Write `docs_chunks` table.
4. **Embed**

   * Deploy an embedding model as a Databricks serving endpoint.
   * Call it from a notebook/job to populate an `embedding` column.
   * Write `docs_chunks_embedded` table (with `id` PK).
5. **Vector Search**

   * Create a Vector Search index over `docs_chunks_embedded.embedding`.
   * Configure endpoint and sync.
6. **RAG chain**

   * Deploy an LLM as a Databricks serving endpoint.
   * Use LangChain:

     * `DatabricksVectorSearch` retriever.
     * `ChatDatabricks` LLM.
     * Prompt template with context injection.
     * Assemble RAG chain.
7. **MLflow**

   * Enable LangChain autolog/tracing.
   * Log the chain as an MLflow model.
   * Register in Unity Catalog.
8. **Serving**

   * Create a Model Serving endpoint for the registered RAG model.
9. **Evaluation**

   * Create an eval app for this endpoint.
   * Collect user feedback.
10. **Productionize**

    * Add guardrails, rate limiting, monitoring.
    * Harden permissions via Unity Catalog.
    * Integrate with your frontends via REST or Lakehouse Apps.
