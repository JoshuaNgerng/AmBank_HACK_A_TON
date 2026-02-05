from typing import Any
from fastapi import APIRouter, Depends, UploadFile, HTTPException, File
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.services.file import file_manager
from app.services.dashboard import update_dashboard, shape_dashboard_info
from app.schemas.dashboard import CompanyInfo, CompanyAnalysis
from app.models.report import CompanyReport, Company
from app.models.dashboard import CompanyDashboard
from app.models.task import TaskProgress
from app.core.database import get_db
from app.core.logging import logger

router = APIRouter()

@router.get('/company', response_model=list[CompanyInfo]) # simple listing
async def get_company(db: Session = Depends(get_db)) -> list[CompanyInfo]:
    company_list = db.execute(select(Company)).scalars().all()
    res = []
    for company in company_list:
        res.append(
            CompanyInfo(
                id=company.id,
                company_id=company.company_id,
                name=company.company_name,
                industry=''
            )
        )
    return res

@router.get('/company/{company_id}/dashboard', response_model=CompanyAnalysis)
async def get_company_detail(
    company_id: int, db: Session = Depends(get_db)
) -> CompanyAnalysis:
    company = db.execute(
        select(Company).where(Company.id == company_id)
    ).scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail=f"Company {company_id} not found")
    company_dashboard = db.execute(
        select(CompanyDashboard).where(CompanyDashboard.company_id == company_id)
    ).scalar_one_or_none()
    if not company_dashboard:
        return await update_company_dashboard(company_id, db)
    if not company_dashboard.summary or not company_dashboard.details:
        return await update_company_dashboard(company_id, db)
    buffer = shape_dashboard_info(company, company_dashboard)
    return CompanyAnalysis.model_validate(buffer)

@router.get('/company/{company_id}/update_dashboard', response_model=CompanyAnalysis)
async def update_company_dashboard(
    company_id: int, db: Session = Depends(get_db)
):
   buffer = update_dashboard(company_id, db)
   return CompanyAnalysis.model_validate(buffer)
