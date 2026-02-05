import json
from datetime import datetime
from typing import Iterable
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models.report import Company, ReportingPeriod
from app.models.analysis import BusinessStrategy, RiskAnalysis, QualitativePerformance, GrowthPotential
from app.models import CompanyDashboard
from app.schemas.dashboard import BusinessStrategyTheme, RiskAssessmentBase, ExecutiveSummary
from app.services.ai_prompt import get_gemini_client, GeminiRateLimitedClient
from pydantic import BaseModel, Field


## AI PLS WORK Keback

class SummaryBusinessStrategy(BusinessStrategyTheme):
    source_ids: list[int] = Field(default_factory=list, description="ids from the db")

class AIBusinessSummary(BaseModel):
    business_sum: list[SummaryBusinessStrategy] = []


sys_prompt = """
You are a finicial assistant helping to summarize and group data
You are reading json representation of the analysis from an annual report

if theres no clear info put an empty list or empty string , DONT MAKE UP info that is not given
"""

def update_dashboard(company_id: int, db: Session):
    company_info = db.execute(
        select(Company).where(Company.id == company_id)
    ).scalar_one_or_none()
    if not company_info:
        raise ValueError(f"Company {company_id} not found")

    past_5_yr = int(datetime.now().year) - 5
    report_info = db.execute(
        select(ReportingPeriod)
        .where(
            (ReportingPeriod.company_id == company_id) &
            (ReportingPeriod.fiscal_year > past_5_yr)
        ).options(
            selectinload(ReportingPeriod.business_strategy),
            selectinload(ReportingPeriod.growth_potential),
            selectinload(ReportingPeriod.qualitative_performance),
            selectinload(ReportingPeriod.risk_analysis)
        )
    ).scalars().all()

    company_dashboard = db.execute(
        select(CompanyDashboard).where(CompanyDashboard.company_id == company_id)
    ).scalar_one_or_none()
    if not company_dashboard:
        company_dashboard = CompanyDashboard(company_id=company_id)
        db.add(company_dashboard)

    # busniess strat sum
    client = get_gemini_client()
    business_sum = adjust_business_sum(report_info, client)
    # risk assesment summary
    risk_assess = adjust_risk_assess(report_info, client)

    # overall summary
    details = {
        "methodology": {
            "signalSelection": "",
            "ordering": "",
            "lookbackYears": 5
        },
        "businessStrategy": business_sum,
        "growthPotential": [report.growth_potential.to_dict() for report in report_info],
        "sentimentAnalysis": [report.qualitative_performance.to_dict() for report in report_info],
        "riskAssessment": risk_assess
    }
    overall = overall_assess(details, client)
    company_dashboard.details = details
    company_dashboard.summary = overall
    db.commit()
    return shape_dashboard_info(company_info, company_dashboard)

def shape_dashboard_info(company: Company, company_dashboard: CompanyDashboard) -> dict:
    overall = company_dashboard.summary
    details = company_dashboard.details
    return {
        "company": {
            "id": company.id,
            "name": company.company_name,
            "industry": str(company.industry),
            "company_id": company.company_id
        },
        "asOf": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lookbackYears": 5,
        "executiveSummary": overall,
        "details": details,
        "citations": []
    }

def adjust_business_sum(report_info: Iterable[ReportingPeriod], client: GeminiRateLimitedClient) -> list[dict]:
    db_data = []
    for report in report_info:
        db_data.append(report.business_strategy.to_dict())
    business_sum = client.single_prompt_answer(sys_prompt, json.dumps(db_data), AIBusinessSummary)
    if business_sum is None:
        raise ValueError(f'AI summarizing busniess info failed')
    assert isinstance(business_sum, AIBusinessSummary)
    buffer_business_sum = []
    for sum in business_sum.business_sum:
        signals = []
        for id_ in sum.source_ids:
            buffer = next((d for d in db_data if d["id"] == id_), None)
            if buffer: signals.append(buffer)
        buffer_2 = sum.model_dump()
        buffer_2.pop('source_ids')
        buffer_2['signals'] = signals
        buffer_business_sum.append(buffer_2)
    return buffer_business_sum

def adjust_risk_assess(report_info: Iterable[ReportingPeriod], client: GeminiRateLimitedClient) -> dict:
    db_data = []
    for report in report_info:
        db_data.append(report.risk_analysis.to_dict())
    risk_assess = client.single_prompt_answer(sys_prompt, json.dumps(db_data), RiskAssessmentBase)
    if risk_assess is None:
        raise ValueError(f'AI summarizing risk assesment failed')
    assert isinstance(risk_assess, RiskAssessmentBase)
    res = risk_assess.model_dump()
    res['factors'] = db_data
    return res

def overall_assess(details: dict, client: GeminiRateLimitedClient) -> dict:
    overall_assessment = client.single_prompt_answer(sys_prompt, json.dumps(details), ExecutiveSummary)
    if overall_assessment is None:
        raise ValueError(f'AI overall assessment failed')
    return overall_assessment.model_dump() # type: ignore
