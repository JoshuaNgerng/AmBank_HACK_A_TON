from typing import Any
from fastapi import APIRouter, Depends, UploadFile, HTTPException, File
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.services.file import file_manager
from app.services.dashboard import update_dashboard, shape_dashboard_info
from app.schemas.dashboard import CompanyListing, CompanyAnalysis, CompanyInfo, CompanyAnalysisResult
from app.models.report import CompanyReport, Company
from app.models.dashboard import CompanyDashboard
from app.models.task import TaskProgress
from app.core.database import get_db
from app.core.logging import logger

router = APIRouter()

@router.get('/company', response_model=CompanyListing)
async def get_company(
    name: str | None = None,
    db: Session = Depends(get_db),
) -> CompanyListing:

    stmt = select(Company)

    if name:
        stmt = (
            stmt
            .where(Company.company_name.ilike(f"%{name}%"))
            .order_by(
                func.similarity(Company.company_name, name).desc()
            )
        )

    companies = db.execute(stmt).scalars().all()

    res = CompanyListing()
    res.data = [
        CompanyInfo(
            id=company.id,
            company_id=company.company_id,
            name=company.company_name,
            industry=str(company.industry) if company.industry else None
        )
        for company in companies
    ]
    return res

@router.get('/company/{company_id}', response_model=CompanyAnalysisResult)
async def get_company_detail(
    company_id: int, db: Session = Depends(get_db)
) -> CompanyAnalysisResult:
    company = db.execute(
        select(Company).where(Company.id == company_id)
    ).scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company {company_id} not found")
    company_dashboard = db.execute(
        select(CompanyDashboard).where(CompanyDashboard.company_id == company_id)
    ).scalar_one_or_none()
    try:
        if not company_dashboard:
            buffer = await update_company_dashboard(company_id, db)
        elif not company_dashboard.summary or not company_dashboard.details:
            buffer = await update_company_dashboard(company_id, db)
        else:
            buffer = shape_dashboard_info(company, company_dashboard)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'updating dashboard failed: {e}')
    return CompanyAnalysisResult(
        success=True,
        data=CompanyAnalysis.model_validate(buffer)
    )

@router.get('/company/{company_id}/update_dashboard', response_model=CompanyAnalysis)
async def update_company_dashboard(
    company_id: int, db: Session = Depends(get_db)
):
   buffer = update_dashboard(company_id, db)
   return CompanyAnalysis.model_validate(buffer)
