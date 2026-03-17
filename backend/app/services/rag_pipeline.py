import os
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
from openai import OpenAI
import uuid

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RAGPipeline:
    # def __init__(self, persist_dir: str = "chroma_store"):
    #     self.client_db = chromadb.PersistentClient(
    #         path=persist_dir,
    #         settings=Settings(anonymized_telemetry=False)
    #     )

    #     self.collection = self.client_db.get_or_create_collection(
    #         name="policy_docs"
    #     )
    def __init__(self):

        self.embedder = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    cache_folder="/tmp"
)

        self.client_db = chromadb.Client(
            Settings(
                persist_directory="data/chroma",
                anonymized_telemetry=False
            )
        )

        self.collection = self.client_db.get_or_create_collection(
            name="policy_docs"
        )

    def chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 150):
        text = " ".join(text.split())  # clean PDF spacing
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap

        return chunks

    def _embed(self, text: str):
        # OpenAI embedding (stable + no download issues)
        resp = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return resp.data[0].embedding

    def ingest_text(self, text: str, source: str):
        chunks = self.chunk_text(text)

        ids, embeddings, metadatas, documents = [], [], [], []

        for i, chunk in enumerate(chunks):
            chunk_id = f"{source}_chunk_{i}_{uuid.uuid4().hex[:6]}"
            emb = self._embed(chunk)

            ids.append(chunk_id)
            embeddings.append(emb)
            documents.append(chunk)
            metadatas.append({"source": source, "chunk_index": i})

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        return {"chunks_added": len(chunks), "source": source}

    def retrieve(self, query: str, top_k: int = 3):
        q_emb = self._embed(query)

        results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        retrieved = []
        for i in range(len(results["documents"][0])):
            retrieved.append({
                "chunk_text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })

        return retrieved
