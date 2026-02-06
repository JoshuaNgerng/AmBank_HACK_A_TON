import json
from typing import Any
from fastapi import APIRouter, Depends, UploadFile, HTTPException, File
from sqlalchemy import select
from sqlalchemy.orm import Session
from celery import chain
from app.celery.ocr import process_pdf, analysis_ocr_result, rerun_analysis_ocr_result
from app.services.file import file_manager
from app.schemas.data_response import ReportProcessingStatus, IncompleteTasks
from app.models.report import CompanyReport
from app.models.task import TaskProgress
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


@router.post('/annual_report', response_model=ReportProcessingStatus)
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

        return ReportProcessingStatus(
            status=f"process file task {report.celery_task_id} sucessfully scheduled"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )

@router.get('/incomplete_task', response_model=list[IncompleteTasks])
def get_all_incomplete_task_id(db: Session = Depends(get_db)):
    data = db.execute(
        select(TaskProgress).where(TaskProgress.complete == False)
    ).scalars().all()
    report_id = set()
    for task in data:
        report_id.add(task.report_id)
    report_info = db.execute(
        select(CompanyReport.id, CompanyReport.file_key)
        .where(CompanyReport.id.in_(report_id))
    ).fetchall()
    res = []
    for task in data:
        print(type(report_info), type(report_info[0]))
        result = next((file for id_, file in report_info if id_ == task.report_id), '')
        res.append(
            IncompleteTasks(
                task_id=task.id, celery_task_id=task.celery_task_id,
                report_id=task.report_id, file_key=result
            )
        )
    return res

@router.get('/rerun_task/{task_id}', response_model=ReportProcessingStatus)
def rerun_task(task_id: int, db: Session = Depends(get_db)):
    task_info = db.execute(
        select(TaskProgress).where(TaskProgress.id == task_id)
    ).scalar_one_or_none()
    if not task_info:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot find task {task_id}"
        )
    task = rerun_analysis_ocr_result.apply_async(args=[task_id]) # type: ignore celery
    return ReportProcessingStatus(
        status=f"rerun processing task {task_id} with celery task {task.id}"
    )    

@router.get('/rerun_report_analysis/{report_id}', response_model=ReportProcessingStatus)
def rerun_analysis(report_id: int, db: Session = Depends(get_db)):
    report_info = db.execute(
        select(CompanyReport)
        .where(CompanyReport.id == report_id)
    ).scalar_one_or_none()
    if not report_info:
        raise HTTPException(status_code=404, detail=f"Company report: {report_id} not found")
    task = analysis_ocr_result.apply_async(args=[report_id, True]) # type: ignore celery
    return ReportProcessingStatus(
        status=f"rerun processing report {report_id} with celery task {task.id}"
    )    
