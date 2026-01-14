import json
from string import Template
from services.azure_ai import single_prompt_answer

template_sys = """
You are analyzing a section from a company's annual report.

Your task is to classify the content into exactly ONE of the following categories:

FINANCIAL_STATEMENTS
- income_statement
- balance_sheet
- cash_flow_statement

POSSIBLE_SIGNALS
- business_strategy         
- growth_potential          
- risk_analysis             
- qualitative_performance   
- market_sentiment          

### Output Schema (STRICT)
{
    "financial_statement": "only one of the three | null",
    "market_signals": ["many possible signals"]
}

Only Return the json schema
Do NOT return explanations.
"""

template_user = Template(
"""
PAGE TEXT:
$text

TABLES:
$tables
"""
)

def classify_ocr_result(data):
    for page_no, info in data.items():
        usr_prompt = template_user.substitute(
            text=info.get('text'), tables=info.get('tables')
        )
        category = single_prompt_answer(template_sys, usr_prompt) or ''
        info['category'] = json.loads(category)
    return data

name_sys = """
You are analyzing a section from a company's annual report.

Your task is to find the company name in this report

Only Return the company name
if NO company name is found Return empty string
Do NOT return explanations.
"""

def extract_company_name(text) -> str:
    return single_prompt_answer(name_sys, text) or ''

name_sys = """
Your task is to find the company name the user is referring to in this request

Only Return the company name
if NO company name is found Return empty string
Do NOT return explanations.
"""

def extract_company_name_user_prompt(text) -> str:
    return single_prompt_answer(name_sys, text) or ''
