import json
from copy import deepcopy
from functools import lru_cache
from string import Template
from app.core.database import from_dict
from app.core.logging import logger
from app.models.report import Company, CompanyReport, ReportingPeriod
from app.models.source import PossibleSignal, Source
from app.models.analysis import (
    BusinessStrategy, RiskAnalysis,
    QualitativePerformance, GrowthPotential
)
from app.schemas.analysis import (
    BusinessStrategyData, RiskAnalysisData,
    QualitativePerformanceData, GrowthPotentialData
)
from app.services.ai_prompt import get_gemini_client
from app.services.organize_section import (
    save_ai_response_schema, flexible_iterator,
    adjust_json_enum_key_2_str, adjust_raw_json_with_enum
)

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
        PossibleSignal.business_strategy: (sys_prompt_business_strategy, BusinessStrategyData, BusinessStrategy),
        PossibleSignal.growth_potential: (sys_prompt_growth_potential, RiskAnalysisData, RiskAnalysis),
        PossibleSignal.risk_analysis: (sys_prompt_risk_analysis, QualitativePerformanceData, QualitativePerformance),
        PossibleSignal.qualitative_performance: (sys_prompt_qualitative_performance, GrowthPotentialData, GrowthPotential)
    }

def prepare_text_analysis(sources: list[Source]):
    data_group : dict[str, list[tuple[str, str, int]]] = {}
    for data in sources:
        if not data.body:
            continue
        for signal in data.signals:
            check = data_group.get(str(signal))
            if not check:
                data_group[str(signal)] = [
                    (data.title or '', data.tables or '', data.id)
                ]
            else:
                check.append((data.title or '', data.tables or '', data.id))
    return data_group

def extract_text_from_sources(
        report: CompanyReport, company: Company,
        data_group: dict[str, list[tuple[str, str, int]]] | None = None,
        start_index: int = 0
):
    mapping = __cache_mapping()
    if not data_group:
        data = prepare_text_analysis(report.report_sources)
    else:
        data = adjust_raw_json_with_enum(data_group, PossibleSignal)
    client = get_gemini_client()
    for idx, type, (sys_prompt, prompt_schema, db_model) in flexible_iterator(mapping, start_index):
        try:
            buffer = data[type]
        except:
            logger.warning(
                f'{report.celery_task_id}, {report.file_key}: {type} not found'
            )
            continue
        usr_prompt = ''
        source_ids = []
        for title, body, source_id in buffer:
            usr_prompt += template_user.substitute(title=title, body=body)
            source_ids.append(source_id)
        response = client.single_prompt_answer(
            sys_prompt=sys_prompt, usr_prompt=usr_prompt,
            response_schema=prompt_schema
        )
        if not response:
            return {'status': False, 'data': adjust_json_enum_key_2_str(data), 'index': idx}
        save_ai_response_schema(
            company, response, db_model, type, # type: ignore
            report.uploaded_at, sources_id=source_ids
        )
    return {'status': True, 'data': None, 'index': None}