from datetime import datetime
import re
from typing import  TypeVar
from difflib import SequenceMatcher
from enum import Enum
import json
from typing import Iterable
from venv import logger
from app.schemas.classify import TextSection, SectionTypes
from app.models.source import Source, FinancialElementBase
from app.models.report import CompanyReport, Company, ReportingPeriod
from app.schemas.shared_identifier import DataListBase, IdentifierBase
from app.core.database import from_dict

def _tokens(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", s.lower()))

E = TypeVar("E", bound=Enum)
def closest_str_enum_match(
    enum: type[E],
    value: str,
    cutoff: float = 0.75,
) -> E | None:
    """
    Find the closest matching Enum member by string value.

    Returns the Enum member or None if confidence is too low.
    """
    if not value:
        return None

    value_tokens = _tokens(value)
    value_norm = value.lower()

    best_score = 0.0
    best_member = None

    for member in enum:
        enum_str = str(member.value)
        enum_tokens = _tokens(enum_str.replace("_", " "))

        token_score = len(value_tokens & enum_tokens) / max(len(enum_tokens), 1)
        seq_score = SequenceMatcher(None, value_norm, enum_str).ratio()

        score = (token_score * 0.6) + (seq_score * 0.4)

        if score > best_score:
            best_score = score
            best_member = member

    return best_member if best_score >= cutoff else None

def group_sections(text_sections: list[TextSection]) -> list[dict[str, str]]:
    res = []
    buffer = {"title": '', "body": '', "tables": ''}
    block = False
    for section in text_sections:
        type_ = section.type
        content = section.content
        if type_ == SectionTypes.doc_title or type_ == SectionTypes.paragraph_title:
            if block == True:
                res.append(buffer)
                buffer = {"title": content, "body": '', "tables": ''}
                block = False
            else:
                buffer['title'] += '\n' + content
            continue
        block = True
        if type_ == SectionTypes.table:
            buffer['tables'] += '\n' + content
            continue
        buffer['body'] += '\n' + content
    if block:
        res.append(buffer)
    return res

def save_text_sections(report: CompanyReport, text_sections: list[list[TextSection]]):
    sources_list = []
    for page_no, section in enumerate(text_sections):
        groups = group_sections(section)
        # if groups:
        #     logger.info(f'debuggin {json.dumps(groups[0], indent=2)}')
        buffer = [from_dict(Source, group) for group in groups]
        for b in buffer: b.page_number = int(page_no)
        sources_list.extend(buffer)
    report.report_sources = sources_list
    logger.info(f'debug total len report sources {len(report.report_sources)}')

def save_ai_response_schema(
        company: Company, response: DataListBase, db_model: type[FinancialElementBase],
        db_field: str, data_date: datetime, default_year: int,
        sources_id: Iterable[int] = []
):
    for statement in response.data:
        assert isinstance(statement, IdentifierBase)
        buffer = statement.model_dump()
        # logger.info(f'converting {json.dumps(buffer, indent=2)}')
        year = statement.year
        if not year: year = default_year
        period = company.get_report_by_year(year)
        if not period:
            period = from_dict(ReportingPeriod, buffer)
            period.fiscal_year = year
            period.report_date = data_date
            company.reporting_period.append(period)
        data = from_dict(db_model, buffer)
        # logger.info(f'conversion result {json.dumps(data.to_dict(), indent=2)}')
        for id_ in sources_id: data.add_source(id_)
        logger.info(f'check typing {type(period)} field: {db_field} data , type {type(data)}')
        setattr(period, db_field, data) # assume the lastest info is the most accurate info

def flexible_iterator(data: dict, start_index=0):
    for i, (key, value) in enumerate(data.items()):
        if i < start_index:
            continue
        yield i, key, value

def adjust_raw_json_with_enum(data: dict, enum: type[Enum]):
    res = {}
    for key, val in data.items():
        try:
            check = enum(key)
            res[check] = val
        except:
            continue
    return res

def adjust_json_enum_key_2_str(data: dict):
    res = {}
    for key, val in data.items():
        res[str(key)] = val
    return res