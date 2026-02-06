import json
from enum import Enum
from datetime import datetime
from typing import Iterable
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models.report import Company, ReportingPeriod
from app.models.analysis import BusinessStrategy, RiskAnalysis, QualitativePerformance, GrowthPotential
from app.models import CompanyDashboard
from app.schemas.dashboard import BusinessStrategyTheme, RiskAssessmentBase, ExecutiveSummary, CompanyAnalysis
from app.services.ai_prompt import get_gemini_client, GeminiRateLimitedClient
from app.core.logging import logger
from pydantic import BaseModel, Field

from datetime import datetime, date
from decimal import Decimal


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

def normalize_types(value):
    """
    Convert:
    - Enum -> its value
    - Decimal -> float
    - datetime/date -> ISO 8601 string

    Works recursively on dicts, lists, tuples, and sets.
    """
    if isinstance(value, Enum):
        return value.value

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, dict):
        return {k: normalize_types(v) for k, v in value.items()}

    if isinstance(value, list):
        return [normalize_types(v) for v in value]

    if isinstance(value, tuple):
        return tuple(normalize_types(v) for v in value)

    if isinstance(value, set):
        return {normalize_types(v) for v in value}

    return value


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
        "growthPotential": [
            normalize_types(report.growth_potential.to_dict())
            for report in report_info if report.growth_potential
        ],
        "sentimentAnalysis": [
            normalize_types(report.qualitative_performance.to_dict())
            for report in report_info if report.qualitative_performance
        ],
        "riskAssessment": risk_assess
    }
    overall = overall_assess(details, client)
    company_dashboard.details = details
    company_dashboard.summary = overall
    data =  shape_dashboard_info(company_info, company_dashboard)
    data = make_sht_up_dashboard(data)
    company_dashboard.overall = normalize_types(data)
    db.commit()
    return data

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

def make_sht_up_dashboard(data: dict) -> dict:
    client = get_gemini_client()
    sys_prompt = """
You are a financial research assistant.

Your task is to analyze and summarize a JSON representation of a company’s financial and business data, grouping related information into clear, structured sections.

If required information is missing, incomplete, or unclear:
- Identify the specific missing fields
- Search the internet for relevant, up-to-date, and reliable information to fill in the gaps
- Prefer primary sources (company filings, investor relations pages, official websites) and reputable secondary sources (financial news outlets, market data providers)

When incorporating external information:
- Clearly distinguish between data derived from the input JSON and data sourced externally
- Cite the source and date for any information obtained from the internet
- If multiple sources disagree, note the discrepancy and provide the most widely accepted or most recent data

If information cannot be reliably found:
- Explicitly state that the data is unavailable or uncertain
- Do not speculate or fabricate values

Return the final output as structured JSON, preserving the original schema and adding only the missing fields that were identified.
"""
    res = client.single_prompt_answer(sys_prompt, json.dumps(data), CompanyAnalysis)
    return res.model_dump() # type: ignore

def adjust_business_sum(report_info: Iterable[ReportingPeriod], client: GeminiRateLimitedClient) -> list[dict]:
    logger.info('check func adjust busniess sum')
    db_data = []
    for report in report_info:
        if report.business_strategy:
            db_data.append(normalize_types(report.business_strategy.to_dict()))
    if not db_data:
        return [
            {
                "theme": "No strategic theme or focus area found",
                "consistencyScore": 0.0,
                "trend": "null",
                "signals": []
            }
        ]
    logger.info('check before prompt')
    business_sum = client.single_prompt_answer(sys_prompt, json.dumps(db_data), AIBusinessSummary)
    if business_sum is None:
        raise ValueError(f'AI summarizing busniess info failed')
    assert isinstance(business_sum, AIBusinessSummary)
    buffer_business_sum = []
    for sum in business_sum.business_sum:
        logger.info(f'summary: {sum.model_dump_json(indent=2)}')
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
        if report.risk_analysis:
            db_data.append(normalize_types(report.risk_analysis.to_dict()))
    if not db_data:
        return {
            "overallScore": 0,
            "posture": "null",
            "summary": "No info on company’s risk profile found",
            "factors": []
        }
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
