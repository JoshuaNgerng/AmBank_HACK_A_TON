from functools import lru_cache
from core.database import from_dict, get_db
from fastapi import APIRouter, Depends, UploadFile, HTTPException, File
from sqlalchemy.orm import Session
from schemas.report import ReportAnalysis
from models.report import ReportAnalysis as ReportAnalysisDB, ClassificationInfo
from models.statements import IncomeStatement, BalanceSheet, CashFlowStatement
from services.ocr import summarize_ocr_result, ocr_report
from services.classify import extract_statement

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
    @lru_cache
    def cache_mapping():
        return {
            'income_statement': IncomeStatement,
            'balance_sheet': BalanceSheet,
            'cash_flow': CashFlowStatement
        }

    # Basic validation
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        # Read file into memory
        pdf_bytes = await file.read()

        # ocr
        ocr_result = ocr_report(pdf_bytes)
        summary = summarize_ocr_result(ocr_result)

        data = ReportAnalysisDB()
        data.pages = len(ocr_result.pages)
        classification_buffer = []
        for page_no, result in summary.items():
            buffer = from_dict(ClassificationInfo, result)
            buffer.page_number = int(page_no)
            classification_buffer.append(buffer)

        # classify and extract
        info = extract_statement(summary)
        mapping = cache_mapping()
        check_dup = set()
        for i in info:
            category = i.get('category')
            if category in check_dup:
                continue
            check_dup.add(category)
            model_ = mapping[category]
            model_info_buffer = from_dict(model_, i)
            model_info_buffer.metadata = i.get('source')
            setattr(data, category, model_info_buffer)
        
        db.add(data)
        db.commit()

        return data.to_dict()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )