import json
from string import Template
from venv import logger
from app.services.ai_prompt import get_gemini_client 
from app.models.source import Source 
from app.schemas.classify import SentimentSignal, Statement

template_sys_signal = """
You are analyzing a section from a company's annual report.

Your task is to classify the content into one or more of the following signals.
Only assign a signal if it is meaningfully supported by the text.

POSSIBLE_SIGNALS

business_strategy:
Statements about long-term direction, competitive positioning, strategic priorities, market focus, or expansion plans.

growth_potential:
Forward-looking discussion of growth opportunities, demand trends, scalability, or future market expansion.

risk_analysis:
Discussion of risks, uncertainties, threats, regulatory challenges, or downside factors.

qualitative_performance:
Narrative assessment of past or current performance, execution quality, operational effectiveness, or management commentary without quantitative metrics.

"""

template_sys_sheet = """
You are analyzing a section from a company's annual report.

You given a html representation of a table and your task is to identify if it fit one of the following

POSSIBLE_STATEMENT

balance_sheet
income_statement
cash_flow

"""

template_usr_data = Template("""
Title:
$title
                             
Content:
$body
""")

def classify_text_section(text_section: Source):
    confidence = 0.0
    remark = ''
    client = get_gemini_client()
    if text_section.tables:
        ans = client.single_prompt_answer(
            sys_prompt=template_sys_sheet, 
            usr_prompt=template_usr_data.substitute(
                title=text_section.title, body=text_section.body
            ),
            response_schema=Statement
        )
        logger.info(f'debugging expected typ Statement {type(ans)}')
        assert isinstance(ans, Statement)
        text_section.statement_type = ans.type
        confidence = ans.confidence
        remark += ans.remarks or ''
    if text_section.body:
        ans = client.single_prompt_answer(
            sys_prompt=template_sys_signal, 
            usr_prompt=template_usr_data.substitute(
                title=text_section.title, body=text_section.body
            ),
            response_schema=SentimentSignal
        )
        if ans is None:
            pass
        logger.info(f'debugging expected typ SentimentSignal {type(ans)}')
        assert isinstance(ans, SentimentSignal)
        text_section.signals = ans.signals
        if not confidence:
            confidence = ans.confidence
        else:
            confidence = (confidence + ans.confidence) / 2
        remark += ans.remarks or ''
    text_section.confidence = confidence
    text_section.classification_remarks = remark

name_sys = """
Your task is to find the company name the user is referring to in this request

Only Return the company name
if NO company name is found Return empty string
Do NOT return explanations.
"""

def extract_company_name_user_prompt(text) -> str:
    return single_prompt_answer(name_sys, text) or '' # type: ignore , its a str
