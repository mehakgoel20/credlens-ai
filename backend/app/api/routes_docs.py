from fastapi import APIRouter, UploadFile, File
from app.utils.pdf_extract import extract_text_from_pdf
from app.services.rag_pipeline import RAGPipeline

router = APIRouter()
rag = RAGPipeline()

@router.post("/upload")
async def upload_doc(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "Only PDF allowed for now"}

    content = await file.read()
    text = extract_text_from_pdf(content)

    ingest_result = rag.ingest_text(text=text, source=file.filename)

    return {
        "filename": file.filename,
        "chunks_added": ingest_result["chunks_added"],
        "text_preview": text[:400]
    }
