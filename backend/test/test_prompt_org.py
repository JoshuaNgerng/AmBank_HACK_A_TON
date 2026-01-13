from string import Template
from unicodedata import category

template_sys = """
You are analyzing pages from a company's annual report.

Classify this page as ONE of:
- income_statement
- balance_sheet
- cash_flow
- notes
- other

Return ONLY the category name.
"""

template_user = Template(
"""
PAGE TEXT:
$text

TABLES:
$tables
"""
)

import json
import sys

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

with open(sys.argv[1], 'r') as f:
    data = json.load(f)

res = {}
for page_no, d in data.items():
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": template_sys
            },
            {
                "role": "user",
                "content": template_user.substitute(text=json.dumps(d.get('text')), tables=json.dumps(d.get('tables')))
            }
        ],
        max_tokens=16384,
        temperature=1.0,
        top_p=1.0,
        model=deployment
    )

    category = response.choices[0].message.content
    print(category)
    d['category'] = category
    res[page_no] = d

with open('debug-res.json', 'w') as f:
    json.dump(res, f, indent=4)