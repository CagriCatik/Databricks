# Ready-to-Deploy RAG endpoint implemented as a custom MLflow pyfunc model for Databricks Model Serving

It assumes:

* You already have:

  * A Mosaic AI Vector Search endpoint + index. ([Microsoft Learn][1])
  * A Databricks-hosted chat LLM endpoint (for example `databricks-dbrx-instruct` or a similar foundation model). ([Databricks Dokumentation][2])
* You will deploy this as a custom model serving endpoint. ([Databricks Dokumentation][3])

You only need to plug in your endpoint/index names and register the model.

---

## 1. RAG model implementation (`rag_endpoint_model.py`)

```python
import os
import textwrap
import requests
import pandas as pd
import mlflow
import mlflow.pyfunc

from databricks.vector_search.client import VectorSearchClient
from databricks.vector_search.utils import CredentialStrategy


class DatabricksRAGModel(mlflow.pyfunc.PythonModel):
    """
    Databricks RAG chatbot model for Model Serving.

    Input (per row):
      question: str          -- user query
      session_id: str|None   -- optional conversation id
      k: int|None            -- optional top-k for retrieval (default 5)

    Output (per row):
      {
        "answer": str,
        "contexts": [str, ...],
        "sources": [str, ...],
        "session_id": str|None
      }

    The model:
      - queries Mosaic AI Vector Search for relevant chunks,
      - builds a prompt with retrieved context,
      - calls a Databricks foundation model chat endpoint,
      - returns the answer plus context metadata.
    """

    def load_context(self, context):
        # Vector search config: set via environment or MLflow model signature parameters
        self.vs_endpoint_name = os.environ["VECTOR_SEARCH_ENDPOINT"]
        self.vs_index_name = os.environ["VECTOR_SEARCH_INDEX"]

        # Foundation model endpoint name (Databricks-hosted chat LLM)
        # Example: "databricks-dbrx-instruct" or "llama-3-70b-instruct"
        self.fm_endpoint_name = os.environ.get(
            "FM_ENDPOINT_NAME",
            "databricks-dbrx-instruct",
        )

        # Workspace URL and auth token for Foundation Model APIs
        # For Model Serving, these can be injected via environment variables
        self.workspace_url = os.environ["DATABRICKS_HOST"].rstrip("/")
        self.workspace_token = os.environ["DATABRICKS_TOKEN"]

        # Configure Vector Search client to use calling user credentials in Model Serving
        # This is the recommended pattern for fine-grained data access control. :contentReference[oaicite:3]{index=3}
        self.vs_client = VectorSearchClient(
            credential_strategy=CredentialStrategy.MODEL_SERVING_USER_CREDENTIALS
        )

        self.vs_index = self.vs_client.get_index(
            endpoint_name=self.vs_endpoint_name,
            index_name=self.vs_index_name,
        )

        # Base system prompt; adjust to your domain
        self.system_prompt = textwrap.dedent(
            """
            You are an enterprise assistant answering questions strictly based
            on the provided context chunks from internal documents.

            Rules:
            - Use only the given context to answer.
            - If the answer is not in the context, say you do not know.
            - Be concise but precise.
            - Include no sensitive information that is not present in context.
            """
        ).strip()

    # ---------- public interface required by mlflow.pyfunc ----------

    def predict(self, context, model_input):
        # Accept either pandas DataFrame or dict-like input
        if isinstance(model_input, dict):
            rows = [model_input]
        elif isinstance(model_input, pd.DataFrame):
            rows = model_input.to_dict(orient="records")
        else:
            raise TypeError("model_input must be a pandas.DataFrame or dict")

        outputs = []
        for row in rows:
            question = row.get("question")
            if not question:
                raise ValueError("Missing required field 'question'")

            session_id = row.get("session_id")
            k = int(row.get("k", 5))

            retrieved = self._retrieve_context(question, k=k)
            context_chunks = retrieved["chunks"]
            sources = retrieved["sources"]

            prompt = self._build_prompt(question, context_chunks)
            answer = self._call_llm(prompt)

            outputs.append(
                {
                    "answer": answer,
                    "contexts": context_chunks,
                    "sources": sources,
                    "session_id": session_id,
                }
            )

        return pd.DataFrame(outputs)

    # ---------- internal helpers ----------

    def _retrieve_context(self, question: str, k: int = 5) -> dict:
        """
        Query Mosaic AI Vector Search for top-k chunks.

        Assumes the index has at least:
          - "chunk_text" column with the text chunk
          - "source" column with document id / URI / path

        Return:
          {
            "chunks": [str, ...],
            "sources": [str, ...]
          }
        """

        # The Python SDK similarity_search API is documented here. :contentReference[oaicite:4]{index=4}
        res = self.vs_index.similarity_search(
            query_text=question,
            columns=["chunk_text", "source"],
            num_results=k,
        )

        # Return format handling.
        # The SDK is a thin wrapper over the REST API which returns JSON
        # with "result" -> "data_array" and "schema" style metadata . :contentReference[oaicite:5]{index=5}
        chunks = []
        sources = []

        # Try data_array format first
        result = res.get("result") or {}
        data_array = result.get("data_array")
        column_names = result.get("column_names") or result.get("schema", {}).get(
            "columns"
        )

        if data_array is not None and column_names is not None:
            # column_names may be list of strings or list of dicts 
            if isinstance(column_names[0], dict):
                col_names = [c["name"] for c in column_names]
            else:
                col_names = column_names

            idx_chunk = col_names.index("chunk_text")
            idx_source = col_names.index("source")

            for row in data_array:
                chunks.append(row[idx_chunk])
                sources.append(row[idx_source])

        else:
            # Fallback: index may already return list-of-dicts style
            # e.g. [{"chunk_text": "...", "source": "..."}] 
            for row in res:
                chunks.append(row["chunk_text"])
                sources.append(row.get("source"))

        return {"chunks": chunks, "sources": sources}

    def _build_prompt(self, question: str, context_chunks) -> str:
        joined_context = "\n\n".join(
            f"[{i+1}] {c}" for i, c in enumerate(context_chunks)
        )

        user_content = textwrap.dedent(
            f"""
            You are answering a user question using the context below.

            Context:
            {joined_context}

            User question:
            {question}

            Answer the question. If you are not sure from the context,
            say you do not know.
            """
        ).strip()

        prompt = f"{self.system_prompt}\n\n{user_content}"
        return prompt

    def _call_llm(self, prompt: str) -> str:
        """
        Calls a Databricks-hosted chat endpoint using the Foundation Model APIs.

        This uses the standard /serving-endpoints/<name>/invocations REST API
        with an OpenAI-compatible chat payload. :contentReference[oaicite:6]{index=6}
        """

        url = f"{self.workspace_url}/serving-endpoints/{self.fm_endpoint_name}/invocations"

        headers = {
            "Authorization": f"Bearer {self.workspace_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 512,
            "temperature": 0.1,
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code != 200:
            raise RuntimeError(
                f"LLM endpoint call failed: {resp.status_code} {resp.text}"
            )

        data = resp.json()

        # Databricks Foundation Model APIs are OpenAI chat-like:
        # data["choices"][0]["message"]["content"] . :contentReference[oaicite:7]{index=7}
        try:
            answer = data["choices"][0]["message"]["content"]
        except Exception as exc:
            raise RuntimeError(f"Unexpected LLM response format: {data}") from exc

        return answer
```

---

## 2. Logging and registering the model in Databricks (`log_rag_model.py`)

Run the following in a Databricks notebook attached to a cluster with `databricks-vectorsearch`, `mlflow`, and `requests` installed. ([Microsoft Learn][1])

Adjust catalog/schema, model name, and environment variables.

```python
import os
import mlflow
from rag_endpoint_model import DatabricksRAGModel

# Workspace-level env values used by the model at serving time.
# In Model Serving you should set these as endpoint environment variables.
os.environ["VECTOR_SEARCH_ENDPOINT"] = "your-vector-search-endpoint-name"
os.environ["VECTOR_SEARCH_INDEX"] = "your_catalog.your_schema.your_index"
os.environ["FM_ENDPOINT_NAME"] = "databricks-dbrx-instruct"
os.environ["DATABRICKS_HOST"] = "https://your-workspace.cloud.databricks.com"
os.environ["DATABRICKS_TOKEN"] = "<your-PAT-or-service-principal-token>"  # do NOT hardcode in production


registered_model_name = "your_catalog.your_schema.rag_endpoint_model"

conda_env = {
    "name": "rag-endpoint-env",
    "channels": ["conda-forge"],
    "dependencies": [
        "python=3.10",
        "pip",
        {
            "pip": [
                "mlflow",
                "requests",
                "databricks-vectorsearch",
            ]
        },
    ],
}

with mlflow.start_run():
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=DatabricksRAGModel(),
        registered_model_name=registered_model_name,
        conda_env=conda_env,
    )

print(f"Registered RAG model as: {registered_model_name}")
```

Notes:

* In production, move secrets (token) into Databricks secrets and configure them as environment variables on the serving endpoint, not in the notebook.
* Unity Catalog 3-level name is required for serving (catalog.schema.model). ([Databricks Dokumentation][3])

---

## 3. Create the serving endpoint

After the model is registered:

1. In the Databricks workspace UI, go to:

   * Machine Learning -> Model Serving -> Create endpoint.
2. Select:

   * Entity type: Registered model.
   * Select the `registered_model_name` from above.
   * Choose a GPU or CPU workload depending on your latency and cost needs. ([Databricks Dokumentation][3])
3. Add environment variables (recommended):

   * VECTOR_SEARCH_ENDPOINT
   * VECTOR_SEARCH_INDEX
   * FM_ENDPOINT_NAME
   * DATABRICKS_HOST
   * DATABRICKS_TOKEN (preferably via a secret reference)

Save and wait until the endpoint is Ready.

You can also create the endpoint via the Databricks CLI or Databricks Python SDK using the `serving-endpoints` API, but the UI path is the shortest. ([MLflow][4])

---

## 4. Example request payload to the RAG endpoint

Once the endpoint is ready, you can invoke it from any client (Teams bot, backend service, curl).

Example `curl`:

```bash
DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
DATABRICKS_TOKEN="dapi-xxx"
ENDPOINT_NAME="rag-chatbot"

curl -s -X POST \
  -H "Authorization: Bearer ${DATABRICKS_TOKEN}" \
  -H "Content-Type: application/json" \
  "${DATABRICKS_HOST}/serving-endpoints/${ENDPOINT_NAME}/invocations" \
  -d '{
    "dataframe_records": [
      {
        "question": "What is our refund policy for enterprise customers?",
        "session_id": "teams-conv-123",
        "k": 5
      }
    ]
  }'
```

The response will be a JSON with a DataFrame-shaped payload from mlflow.pyfunc:

```json
{
  "predictions": [
    {
      "answer": "Text of the answer...",
      "contexts": ["chunk 1...", "chunk 2..."],
      "sources": ["doc://policy.pdf#p3", "doc://policy.pdf#p4"],
      "session_id": "teams-conv-123"
    }
  ]
}
```

The Teams bot can take `answer` as the message text and optionally render `sources` as citations in Adaptive Cards.

---

This endpoint is now ready to sit behind your Teams bot or any other client that needs a Databricks RAG-backed chat interface.

[1]: https://learn.microsoft.com/en-us/azure/databricks/generative-ai/create-query-vector-search?utm_source=chatgpt.com "How to create and query a vector search index - Azure Databricks"
[2]: https://docs.databricks.com/aws/en/machine-learning/foundation-model-apis/api-reference?utm_source=chatgpt.com "Foundation model REST API reference - Databricks on AWS"
[3]: https://docs.databricks.com/aws/en/machine-learning/model-serving/create-manage-serving-endpoints?utm_source=chatgpt.com "Create custom model serving endpoints - Databricks on AWS"
[4]: https://mlflow.org/docs/latest/api_reference/_modules/mlflow/deployments/databricks.html?utm_source=chatgpt.com "mlflow.deployments.databricks"
