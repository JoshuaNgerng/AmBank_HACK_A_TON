import json
from string import Template
from typing import Any
from decimal import Decimal
from services.ai_prompt import single_prompt_answer

system_prompt = """
You are Financial Analyst Assistant and company info is a json from a database

You are to answer in easily understandable language with the info avaiable 
You are to state your assumptions and possible missing data if you cannot answer with confidence
"""

user_prompt_template = Template("""
COMPANY_INFO:
$company_info
                       
USER_PROMPT:
$user_prompt
""")


def convert_decimals_to_str(d):
    """
    Recursively converts all Decimal values in a dictionary to strings.
    
    Args:
        d (dict): The input dictionary (can contain nested dicts or lists).
    
    Returns:
        dict: A new dictionary with Decimals converted to strings.
    """
    if isinstance(d, dict):
        return {k: convert_decimals_to_str(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [convert_decimals_to_str(item) for item in d]
    elif isinstance(d, Decimal):
        return str(d)
    else:
        return d

def ask_ai_about_company(user_prompt: str, company_info: dict[str, Any]):
    info = convert_decimals_to_str(company_info)
    return single_prompt_answer(system_prompt, user_prompt_template.substitute(company_info=json.dumps(info), user_prompt=user_prompt))