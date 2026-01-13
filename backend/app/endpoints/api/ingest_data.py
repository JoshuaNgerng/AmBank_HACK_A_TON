from models.base import Base
from core.database import engine, get_db
from fastapi import APIRouter, Depends, UploadFile, HTTPException, File
from sqlalchemy.orm import Session
from schemas.report import ReportAnalysis
import fitz  # PyMuPDF

router = APIRouter()

@router.post("/annual_report/test_pages")
async def test_pdf_pages(file: UploadFile = File(...)):
    # Basic validation
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        # Read file into memory
        pdf_bytes = await file.read()

        # Open PDF from bytes
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            page_count = doc.page_count

        return {
            "filename": file.filename,
            "pages": page_count
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )


@router.post('/annual_report', response_model=ReportAnalysis)
async def ingest_annual_report(
    file: UploadFile, 
    db: Session = Depends(get_db)
):
    return ReportAnalysis(status="not yet implemented")