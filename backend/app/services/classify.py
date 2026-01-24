import json
from string import Template
from services.ai_prompt import single_prompt_answer

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

def classify_ocr_result(data):
    for page_no, info in data.items():
        usr_prompt = template_user.substitute(
            text=info.get('text'), tables=info.get('tables')
        )
        category = single_prompt_answer(template_sys, usr_prompt) or ''
        info['category'] = json.loads(category)
    return data


name_sys = """
Your task is to find the company name the user is referring to in this request

Only Return the company name
if NO company name is found Return empty string
Do NOT return explanations.
"""

def extract_company_name_user_prompt(text) -> str:
    return single_prompt_answer(name_sys, text) or ''
