import json
from typing import Any
from fastapi import APIRouter, Depends, UploadFile, HTTPException, File
from sqlalchemy.orm import Session
from celery import chain
from app.celery.ocr import process_pdf, analysis_ocr_result
from app.services.file import file_manager
from app.models.report import CompanyReport
from app.core.database import get_db
from app.core.logging import logger

router = APIRouter()

@router.get('/test_storage', response_model=dict[str, Any])
async def test_dir(
    # file: UploadFile, 
    # db: Session = Depends(get_db)
):
    print(file_manager.file_root)
    return {"dir": file_manager.file_root}


@router.post('/annual_report', response_model=dict[str, Any])
async def ingest_annual_report(
    file: UploadFile, 
    db: Session = Depends(get_db)
):
    # Basic validation
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        # make a company report and pass its id to celery ocr task
        report = CompanyReport()
        pdf_bytes = await file.read()
        report.file_key = file_manager.upload_file(pdf_bytes, file.filename, None)
        # report.total_pages = 0
        db.add(report)
        db.commit()
        # logger.info(f'debugging {type(process_pdf)}, {type(analysis_ocr_result)}')
        workflow = chain(process_pdf.s(report.id), analysis_ocr_result.s()).apply_async() # type: ignore
        # save celery task id into company report
        report.celery_task_id = workflow.id # type: ignore
        db.commit()

        return {"status": f"process file task {report.celery_task_id} sucessfully scheduled"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )