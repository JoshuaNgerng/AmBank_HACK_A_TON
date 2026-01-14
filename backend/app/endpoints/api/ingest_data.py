from functools import lru_cache
import json
from typing import Any
from venv import logger
from core.database import from_dict, get_db
from fastapi import APIRouter, Depends, UploadFile, HTTPException, File
from sqlalchemy.orm import Session
from models.report import ReportAnalysis as ReportAnalysisDB, ClassificationInfo
from models.statements import IncomeStatement, BalanceSheet, CashFlowStatement
from models.analysis import BusinessStrategy, RiskAnalysis, QualitativePerformance, GrowthPotential
from services.ocr import summarize_ocr_result, ocr_report
from services.classify import classify_ocr_result, extract_company_name
from services.extract import extract_statement
from services.text_analysis import extract_text_signal

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


@router.post('/annual_report', response_model=dict[str, Any])
async def ingest_annual_report(
    file: UploadFile, 
    db: Session = Depends(get_db)
):
    @lru_cache
    def cache_mapping_fs():
        return {
            'income_statement': IncomeStatement,
            'balance_sheet': BalanceSheet,
            'cash_flow': CashFlowStatement
        }

    @lru_cache
    def cache_mapping_ms():
        return {
            'business_strategy': BusinessStrategy,
            'risk_analysis': RiskAnalysis,
            'qualitative_performance': QualitativePerformance,
            'growth_potential': GrowthPotential
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
        data.company_name = extract_company_name(ocr_result.content[:200])
        classification_buffer = []
        for page_no, result in summary.items():
            buffer = from_dict(ClassificationInfo, result)
            buffer.page_number = int(page_no)
            classification_buffer.append(buffer)

        # classify and extract
        classified_summary = classify_ocr_result(summary)
        # try:
        info = extract_statement(classified_summary)
        # except Exception as e:
            # logger.error(f'debugging error: {json.dumps(classified_summary, indent=4)}')
            # raise
        mapping = cache_mapping_fs()
        check_dup = set()
        for i in info:
            category = i.get('category')
            if category in check_dup:
                continue
            check_dup.add(category)
            model_ = mapping[category]
            model_info_buffer = from_dict(model_, i)
            setattr(data, category, model_info_buffer)
        
        try:
            logger.info('process text signal')
            logger.info(f'debug: {classified_summary.keys()}')
            info = extract_text_signal(classified_summary)
            mapping = cache_mapping_ms()
            # logger.info(f'debugging: {json.dumps(info, indent=2)}')
            for signal, i in info.items():
                logger.info(f'triiger loop: {signal}')
                if signal not in mapping:
                    continue
                model_ = mapping[signal]
                model_info_buffer = from_dict(model_, i.get('data'))
                model_info_buffer.sources = i.get('sources')
                setattr(data, signal, model_info_buffer)
        except Exception as e:
            logger.error(e)
            raise

        db.add(data)
        db.commit()

        return data.to_dict()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )