from copy import deepcopy
from string import Template

template_income_sys = """
You are analyzing the income statement from a company's annual report.

MUST return a json format , no additional comments
MUST be in the following schema

{
    "revenue": 135220000,
    "cost_of_goods_sold": 48900000,
    "gross_profit": 86320000,

    "operating_expenses": 33400000,
    "operating_income": 52920000,

    "finance_costs": 4200000,
    "profit_before_tax": 48720000,

    "tax": 8200000,
    "net_income": 40520000,

    "eps": 0.12,
    "period": 20/01/2000
}
"""

template_balance_sys = """
You are analyzing the income statement from a company's annual report.

MUST return a json format , no additional comments
MUST be in the following schema

{
    "current_assets": 210300000,
    "non_current_assets": 364700000,
    "total_assets": 575000000,

    "current_liabilities": 135000000,
    "non_current_liabilities": 185000000,
    "total_liabilities": 320000000,

    "equity": 255000000,
    "period": 20/01/2000
}
"""

template_cash_sys = """
You are analyzing the income statement from a company's annual report.

MUST return a json format , no additional comments
MUST be in the following schema

{
    "operating_cash_flow": 55300000,
    "investing_cash_flow": -21200000,
    "financing_cash_flow": -8700000,

    "net_change_in_cash": 25400000,
    "beginning_cash": 61300000,
    "ending_cash": 86700000,
    "period": 20/01/2000
}
"""

template_user = Template(
"""
PAGE TEXT:
$text

TABLES:
$tables
"""
)

import os
from openai import AzureOpenAI

endpoint = os.getenv('AZURE_TARGET_URL', '')
model_name = "gpt-5-chat"
deployment = "gpt-5-chat"

subscription_key = os.getenv('AZURE_API_KEY', '')
api_version = "2024-12-01-preview"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

def prompt_ai(template_sys: str, text, tables):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": template_sys
            },
            {
                "role": "user",
                "content": template_user.substitute(text=json.dumps(text), tables=json.dumps(tables))
            }
        ],
        max_tokens=16384,
        temperature=1.0,
        top_p=1.0,
        model=deployment
    )
    return response.choices[0].message.content

def merge_data(current, new, page_no):
    if current is None:
        current = deepcopy(new)
        current['source'] = [page_no]
        return current
    current['text'] += new['text']
    current['tables'].extend(new['tables'])
    current['source'].append(page_no)
    return current

def cleanup_statement_info(data):
    res = []
    categories = {'income_statement', 'balance_sheet', 'cash_flow'}
    buffer = None
    prev_c = None
    for page_no, info in data.items():
        c = info.get('category')
        # print(c)
        # print(c, prev_c)
        if c not in categories:
            # print('check1', c, prev_c)
            if not buffer:
                continue
            res.append(buffer)
            buffer = None
            prev_c = c
            continue
        if prev_c is None:
            # print('check2', c, prev_c)
            buffer = merge_data(buffer, info, page_no)
            prev_c = c
            continue
        if prev_c == c:
            # print('check3', c, prev_c)
            buffer = merge_data(buffer, info, page_no)
        if prev_c not in categories:
            # print('check4', c, prev_c)
            buffer = merge_data(buffer, info, page_no)
        prev_c = c
    if buffer:
        res.append(buffer)
    return res


def extract_statement(data):
    categories = {
        'income_statement': template_income_sys,
        'balance_sheet': template_balance_sys,
        'cash_flow': template_cash_sys
    }
    res = []
    for d in data:
        c = d.get('category')
        buffer = prompt_ai(categories[c], d.get('text'), d.get('tables'))
        assert buffer is not None
        buffer_ = json.loads(buffer) 
        buffer = { 'category': c, 'source': d.get('source') }
        buffer['data'] = buffer_
        res.append(buffer)
    return res

if __name__ == '__main__':
    import json
    import sys

    with open('debug-res.json', 'r') as f:
        data = json.load(f)
    cleaned_data = cleanup_statement_info(data)
    res = extract_statement(cleaned_data)
    with open('fin-res.json', 'w') as f:
        json.dump(res, f, indent=4)