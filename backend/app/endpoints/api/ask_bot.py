from fastapi import APIRouter, Depends
from sqlalchemy import Select
from sqlalchemy.orm import Session, selectinload
from app.core.database import from_dict, get_db
from app.schemas.ask_bot import UserQuestion
from app.models.report import Company
from app.services.classify import extract_company_name_user_prompt
from app.services.search_db import find_closest_companies
from app.services.ai_analysis import ask_ai_about_company

router = APIRouter()

@router.post('/ask', response_model=str)
async def ask_bot(question: UserQuestion, db: Session = Depends(get_db)) -> str:
    # company_name = extract_company_name_user_prompt(question.prompt)
    # if not company_name:
    #     return f"We cannot infer what company you're referring to"
    # company_info = db.execute(
    #     Select(ReportAnalysis)
    #     .where(ReportAnalysis.company_name == company_name)
    #     .options(
    #         selectinload(ReportAnalysis.income_statement),
    #         selectinload(ReportAnalysis.balance_sheet),
    #         selectinload(ReportAnalysis.cash_flow),
    #         selectinload(ReportAnalysis.business_strategy),
    #         selectinload(ReportAnalysis.risk_analysis),
    #         selectinload(ReportAnalysis.growth_potential),
    #         selectinload(ReportAnalysis.qualitative_performance),
    #     )
    #     .order_by(ReportAnalysis.created_at.asc())
    # ).scalars().first()
    # if not company_info:
    #     likely_company = find_closest_companies(db, company_name)
    #     likely_company = [l.get('company_name') for l in likely_company]
    #     if not likely_company:
    #         return f"We cannot find {company_name} in the database, you can upload the company's finicial report to update the database"
    #     return f"{company_name} doesn't match any company in the database, but here are some likely candidates: {likely_company}"
    # assert isinstance(company_info, ReportAnalysis)
    # buffer = company_info.to_dict()
    # if company_info.income_statement:
    #     buffer['income_statement'] = company_info.income_statement.to_dict()
    # if company_info.balance_sheet:
    #     buffer['balance_sheet'] = company_info.balance_sheet.to_dict()
    # if company_info.cash_flow:
    #     buffer['cash_flow'] = company_info.cash_flow.to_dict()
    # if company_info.business_strategy:
    #     buffer['business_strategy'] = company_info.business_strategy.to_dict()
    # if company_info.risk_analysis:
    #     buffer['risk_analysis'] = company_info.risk_analysis.to_dict()
    # if company_info.growth_potential:
    #     buffer['growth_potential'] = company_info.growth_potential.to_dict()
    # if company_info.qualitative_performance:
    #     buffer['qualitative_performance'] = company_info.qualitative_performance.to_dict()
    # return  ask_ai_about_company(question.prompt, buffer) or ''
    return ''