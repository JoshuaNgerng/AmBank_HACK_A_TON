import json
from copy import deepcopy
from functools import lru_cache
from string import Template
from app.core.database import from_dict
from app.core.logging import logger
from app.models.report import Company, CompanyReport, ReportingPeriod
from app.models.analysis import (
    BusinessStrategy, RiskAnalysis,
    QualitativePerformance, GrowthPotential
)
from app.schemas.analysis import (
    BusinessStrategyData, RiskAnalysisData,
    QualitativePerformanceData, GrowthPotentialData
)
from app.services.ai_prompt import single_prompt_answer
from app.services.organize_section import save_ai_response_schema

sys_prompt_business_strategy = """
You are a corporate strategy analyst.

Analyze the following text from a company's annual report.

Extract ONLY information related to:
- what the company is trying to achieve
- its business focus
- its positioning
- its strategic direction
- how it differentiates itself

Ignore risks, financial figures, and general background.

Do not fabricate.
Use null or empty arrays if information is missing.
MUST return a json format , no additional comments
MUST be in the following schema
"""

sys_prompt_risk_analysis = """
You are a risk and compliance analyst.

Analyze the following text from a company's annual report.

Extract ONLY:
- risks
- uncertainties
- exposures
- weaknesses
- how the company discusses managing those risks

Do not include strategy, growth, or financial metrics.
Do not fabricate.
Use null or empty arrays if information is missing.

"""

sys_prompt_market_sentiment = """
You are a market sentiment analyst.

Analyze the tone and confidence expressed in this text.

Extract:
- how positive or negative management sounds
- how confident they appear about the future
- signals of optimism, caution, or uncertainty

Do not fabricate.
Use null or empty arrays if information is missing.
MUST return a json format , no additional comments
MUST be in the following schema
"""

sys_prompt_qualitative_performance = """
You are an operations and execution analyst.

Analyze the text for how well the company describes:
- its operations
- execution
- stability
- efficiency
- ability to deliver

Ignore strategy, growth plans, and risks.

Do not fabricate.
Use null or empty arrays if information is missing.
MUST return a json format , no additional comments
MUST be in the following schema
"""

sys_prompt_growth_potential = """
You are a growth and opportunity analyst.

Analyze the text for:
- future expansion
- demand
- opportunities
- market size
- constraints on growth

Do not fabricate.
Use null or empty arrays if information is missing.
MUST return a json format , no additional comments
MUST be in the following schema
"""

template_user = Template("""
TITLE
$title

BODY
$body
""")

@lru_cache
def __cache_mapping():
    return {
        'business_strategy': (sys_prompt_business_strategy, BusinessStrategyData, BusinessStrategy),
        'growth_potential': (sys_prompt_growth_potential, RiskAnalysisData, RiskAnalysis),
        'risk_analysis': (sys_prompt_risk_analysis, QualitativePerformanceData, QualitativePerformance),
        'qualitative_performance': (sys_prompt_qualitative_performance, GrowthPotentialData, GrowthPotential)
    }

def extract_text_from_sources(report: CompanyReport, company: Company):
    check_dup = set()
    mapping = __cache_mapping()
    data_group : dict[str, list[tuple[str, str, int]]]= {}
    for data in report.report_sources:
        if not data.tables or data.statement_type not in mapping:
            continue
        if data.statement_type in check_dup:
            continue
        check_dup.add(data.statement_type)
        data_group[str(data.statement_type)].append((data.title, data.tables, data.id))
        # assume only one source of statement is valid
    for type, (sys_prompt, prompt_schema, db_model) in mapping.items():
        try:
            buffer = data_group[type]
        except:
            logger.warning(f'{report.celery_task_id}, {report.file_key}: {type} not found')
            continue
        usr_prompt = ''
        source_ids = []
        for title, body, source_id in buffer:
            usr_prompt += template_user.substitute(title=title, body=body)
            source_ids.append(source_id)
        response = single_prompt_answer(
            sys_prompt=sys_prompt, usr_prompt=usr_prompt, response_schema=prompt_schema
        )
        save_ai_response_schema(
            company, response, db_model, # type: ignore
            type, report.uploaded_at, source_ids
        )
