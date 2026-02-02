from http import client
import json
from copy import deepcopy
from string import Template
from functools import lru_cache
from app.core.database import from_dict
from app.core.logging import logger
from app.services.ai_prompt import get_gemini_client
from app.services.organize_section import flexible_iterator, save_ai_response_schema
from app.models.report import Company, CompanyReport, ReportingPeriod, Source
from app.models.source import FinicialElementBase
from app.models.statements import IncomeStatement, BalanceSheet, CashFlowStatement
from app.schemas.statements import IncomeStatements, BalanceSheets, CashFlowStatments 
from app.schemas.shared_identifier import IdentifierBase, DataListBase

template_income_sys = """
You are analyzing the income statement from a company's annual report.
The tables are represented in html form
"""

template_balance_sys = """
You are analyzing the income statement from a company's annual report.
The tables are represented in html form
"""

template_cash_sys = """
You are analyzing the income statement from a company's annual report.
The tables are represented in html form
"""

template_user = Template(
"""
TITLE:
$title

TABLES:
$tables
"""
)

@lru_cache
def __cache_mapping():
    return {
        'income_statement': (template_income_sys, IncomeStatements, IncomeStatement),
        'balance_sheet': (template_balance_sys, BalanceSheets, BalanceSheet),
        'cash_flow_statement': (template_cash_sys, CashFlowStatments, CashFlowStatement)
    }

def prepare_statement_data(sources: list[Source]):
    check_dup = set()
    mapping = __cache_mapping()
    data_group : dict[str, tuple[str, str, int]]= {}
    for data in sources:
        if not data.tables or data.statement_type not in mapping:
            continue
        if data.statement_type in check_dup:
            continue
        check_dup.add(data.statement_type)
        data_group[str(data.statement_type)] = (data.title, data.tables, data.id)
        # assume only one source of statement is valid
    return data_group


def extract_statement_from_sources(
        report: CompanyReport, company: Company,
        data_group: dict[str, tuple[str, str, int]] | None = None,
        resume_index: int = 0
):
    mapping = __cache_mapping()
    client = get_gemini_client()
    if not data_group:
        data_group = prepare_statement_data(report.report_sources)
    for type, (sys_prompt, prompt_schema, db_model) in flexible_iterator(mapping, resume_index):
        try:
            title, table, id_ = data_group[type]
        except:
            logger.warning(f'{report.celery_task_id}, {report.file_key}: {type} not found')
            continue
        usr_prompt = template_user.substitute(title=title, tables=table)
        response = client.single_prompt_answer(
            sys_prompt=sys_prompt, usr_prompt=usr_prompt, response_schema=prompt_schema
        )
        if not response:
            return {'status': False, 'data': data_group}
        save_ai_response_schema(company, response, db_model, type, (id_,), report.uploaded_at) # type: ignore
        return {'status': True, 'data': None}
