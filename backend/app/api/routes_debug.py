from fastapi import APIRouter
from app.services.rag_pipeline import RAGPipeline

router = APIRouter()
rag = RAGPipeline()

@router.get("/count")
def count_docs():
    return {"count": rag.collection.count()}
