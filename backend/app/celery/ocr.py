from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.celery import celery_app
from app.core.database import get_db_session
from app.core.logging import logger
from app.services.ocr import ocr_pdf_report
from app.services.file import file_manager
from app.services.get_company import get_company_info
from app.services.organize_section import save_text_sections
from app.services.classify import classify_text_section 
from app.services.extract_statement import extract_statement_from_sources
from app.services.text_analysis import extract_text_from_sources
from app.models.report import Company, CompanyReport

assert celery_app is not None

@celery_app.task(bind=True, name="ocr.process_pdf")
def process_pdf(self, report_id: int):
    with get_db_session() as db:
        report = db.execute(
            select(CompanyReport)
            .where(CompanyReport.id == report_id)
        ).scalar_one_or_none()
        if not report:
            raise ValueError(f'Cannot retrieve CompanyReport {report_id}')
        pdf_bytes = file_manager.download_file(report.file_key)
        if not pdf_bytes:
            raise ValueError(f'Cannot retrieve file content {report.file_key}')
        ocr_result, page_count = ocr_pdf_report(pdf_bytes)
        company_info = get_company_info(ocr_result)
        logger.info(company_info)
        if not company_info.company_name and not company_info.resigtration_no:
            raise ValueError("Both company name and resigtration no unable to indentify")
        company = db.execute(
            select(Company).where(Company.company_id == company_info.resigtration_no)
        ).scalar_one_or_none()
        if not company:
            company = db.execute(
                select(Company)
                .where(Company.company_name == company_info.company_name)
            ).scalar_one_or_none()
        if not company:
            company = Company(
                company_id=company_info.resigtration_no,
                company_name=company_info.company_name
            )
            db.add(company)
        report.total_pages = page_count
        # return {'status': 'debug here'}
        save_text_sections(report, ocr_result)
        company.company_reports.append(report)
        logger.info(f'before saving company report {report.file_key}')
        db.commit()
        return report_id
    
@celery_app.task(bind=True, name="ocr.analysis_pdf")
def analysis_ocr_result(self, report_id: int):
    with get_db_session() as db:
        report = db.execute(
            select(CompanyReport)
            .where(CompanyReport.id == report_id)
            .options(selectinload(CompanyReport.company))
        ).scalar_one_or_none()
        if not report:
            raise ValueError(f'Cannot retrieve company report {report_id}')

        for section in report.report_sources:
            classify_text_section(section)

        extract_statement_from_sources(report, report.company)
        extract_text_from_sources(report, report.company)

        db.commit()

@celery_app.task(bind=True, name="ocr.rerun_analysis")
def rerun_analysis_ocr_result(self, task_id: int):
    with get_db_session() as db:
        db.commit()
    