from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_pipeline import RAGPipeline

router = APIRouter()
rag = RAGPipeline()

class QueryInput(BaseModel):
    query: str

@router.post("/")
def retrieve_policy(data: QueryInput):
    results = rag.retrieve(data.query, top_k=3)
    return {"query": data.query, "results": results}
