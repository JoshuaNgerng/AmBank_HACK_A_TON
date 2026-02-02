from datetime import datetime
import json
from typing import Iterable
from venv import logger
from app.schemas.classify import TextSection, SectionTypes
from app.models.source import Source, FinicialElementBase
from app.models.report import CompanyReport, Company, ReportingPeriod
from app.schemas.shared_identifier import DataListBase, IdentifierBase
from app.core.database import from_dict

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
        company: Company, response: DataListBase, db_model: type[FinicialElementBase],
        db_field: str, data_date: datetime, sources_id: Iterable[int] = []
):
    for statement in response.data:
        assert isinstance(statement, IdentifierBase)
        buffer = statement.model_dump()
        year = statement.year
        if not year: continue
        period = company.get_report_by_year(year)
        if not period:
            period = from_dict(ReportingPeriod, buffer)
            period.report_date = data_date
            company.reporting_period.append(period)
        data = from_dict(db_model, buffer)
        for id_ in sources_id: data.add_source(id_)
        setattr(period, db_field, data) # assume the lastest info is the most accurate info

def flexible_iterator(data: dict, start_index=0):
    for i, (key, value) in enumerate(data.items()):
        if i < start_index:
            continue
        yield key, value
