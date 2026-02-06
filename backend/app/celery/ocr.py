from datetime import datetime
from functools import lru_cache
from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session
from typing import Any

from app.core.celery import celery_app
from app.core.database import get_db_session
from app.core.logging import logger
from app.services.ocr import ocr_pdf_report
from app.services.file import file_manager
from app.services.get_company import get_company_info 
from app.services.organize_section import save_text_sections, closest_str_enum_match
from app.services.classify import classify_text_sections
from app.services.extract_statement import extract_statement_from_sources
from app.services.text_analysis import extract_text_from_sources
from app.models.report import Company, CompanyReport, Industry
from app.models.source import Source 
from app.models.task import TaskProgress, ProgressState

assert celery_app is not None

class ProgressException(Exception):
    def __init__(self, message: str, data: Any, index: int):
        super().__init__(message)
        self.message = message
        self.data = data
        self.index = index

    def __str__(self):
        return self.message

def identify_company(data: list[Source], db: Session) -> tuple[Company, int]:
    company_info = get_company_info(data)
    # logger.info(company_info)
    if not company_info:
        raise ValueError(f'Company Identification Failed')
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
            company_name=company_info.company_name,
            industry=(
                closest_str_enum_match(Industry, company_info.industry)
                if company_info.industry else None
            )
        )
        db.add(company)
    if not company.company_id and company_info.resigtration_no:
        company.company_id = company_info.resigtration_no
    if not company.industry and company_info.industry:
        company.industry = closest_str_enum_match(Industry, company_info.industry)
    fiscal_year = company_info.fiscal_year or int(datetime.now().year) - 1
    return company, fiscal_year

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
        report.total_pages = page_count
        save_text_sections(report, ocr_result)
        company, fiscal_year = identify_company(report.report_sources, db)
        company.company_reports.append(report)
        report.report_year = fiscal_year
        logger.info(f'before saving company report {report.file_key}')
        db.commit()
        return report_id

@celery_app.task(bind=True, name="ocr.analysis_pdf")
def analysis_ocr_result(self, report_id: int, skip_classification_text: bool = False):
    with get_db_session() as db:
        report = db.execute(
            select(CompanyReport)
            .where(CompanyReport.id == report_id)
            .options(
                selectinload(CompanyReport.company, Company.reporting_period)
            )
        ).scalar_one_or_none()
        if not report:
            raise ValueError(f'Cannot retrieve company report {report_id}')
        task = TaskProgress(celery_task_id=self.request.root_id, report_id=report.id)
        db.add(task)
        db.commit()
        try:
            if not skip_classification_text:
                check = classify_text_sections(report.report_sources)
                if not check['status']:
                    raise ProgressException(
                        message='classification text section error',
                        data=None,
                        index=check['index']
                    )
            else:
                logger.info(f'skipped classify text section')
            # check = extract_statement_from_sources(
            #     report, report.company, expected_year=report.report_year
            # )
            # if not check['status']:
            #     raise ProgressException(
            #         message='extract statement error',
            #         data=check['data'],
            #         index=check['index']
            #     )
            check = extract_text_from_sources(
                report, report.company, expected_year=report.report_year
            )
            if not check['status']:
                raise ProgressException(
                    message='extract text error',
                    data=check['data'],
                    index=check['index']
                )
        except ProgressException as e:
            task.immediatory_state = e.data
            task.index = e.index
            db.commit()
            raise
        except Exception as e:
            logger.error(f'Unknown error: {e}')
            db.commit()

        task.complete = True
        db.commit()

@celery_app.task(bind=True, name="ocr.rerun_analysis")
def rerun_analysis_ocr_result(self, task_id: int):
    @lru_cache
    def cache_mapping():
        def wrapper_classify_text_sections(
            report: CompanyReport,
            company: Company,
            expected_year: int = 0,
            data_group: dict[str, tuple[str, str, int]] | None = None,
            resume_index: int = 0
        ):
            return classify_text_sections(report.report_sources, resume_index)
        return {
            ProgressState.classify: (wrapper_classify_text_sections, 'classification text section error'),
            ProgressState.statement: (extract_statement_from_sources, 'extract statement error'),
            ProgressState.analysis: (extract_text_from_sources, 'extract text error'),
        }
    mapping = cache_mapping()
    with get_db_session() as db:
        task = db.execute(
            select(TaskProgress).where(TaskProgress.celery_task_id == task_id)
        ).scalar_one_or_none()
        if not task:
            raise ValueError(f'Cannot find task progress {task_id}')
        report = db.execute(
            select(CompanyReport)
            .where(CompanyReport.id == task.report_id)
            .options(selectinload(CompanyReport.company))
        ).scalar_one_or_none()
        if not report:
            raise ValueError(f'Cannot retrieve company report {task.report_id}')
        if not report.company:
            report.company, year = identify_company(report.report_sources, db)
            report.report_year = year
        try:
            progress = task.progress
            index = task.index or 0
            for state in ProgressState:
                if progress == state or not progress:
                    func, msg = mapping[state]
                    check = func(
                        report, report.company, task.immediatory_state, 
                        expected_year=report.report_year,
                        resume_index=index
                    )
                    if not check['status']:
                        raise ProgressException(
                            message=msg,
                            data=check['data'],
                            index=check['index']
                        )
                    progress = None
                    index = 0
        except ProgressException as e:
            task.immediatory_state = e.data
            task.index = e.index
            db.commit()
            raise
        db.commit()
