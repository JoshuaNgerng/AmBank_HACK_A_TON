import json
import sys
from venv import logger
from core.config import settings
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, DocumentTable
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

client = DocumentIntelligenceClient(
    endpoint=settings.AZURE_DOC_URL,
    credential=AzureKeyCredential(settings.AZURE_DOC_KEY)
)

def ocr_report(data: bytes):
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        AnalyzeDocumentRequest(bytes_source=data)
    )

    result = poller.result()
    logger.info(f"Model: {result.model_id}, pages returned: {len(result.pages)}")

    return result

def table_to_struct(table: DocumentTable):
    grid = [[None]*table.column_count for _ in range(table.row_count)]
    for cell in table.cells:
        grid[cell.row_index][cell.column_index] = cell.content.strip() # type: ignore

    header = tuple(grid[0])   # first row is column header
    return {
        "grid": grid,
        "header": header,
        "columns": table.column_count
    }


def summarize_ocr_result(result: AnalyzeResult):
    pages = {}

    for i in range(len(result.pages)):
        pages[i + 1] = {'text': '', 'tables': []}

    # Text
    for p in result.pages:
        if p.lines is None: continue
        pages[p.page_number]["text"] = "\n".join(l.content for l in p.lines)

    # Tables
    if result.tables is None: result.tables = []
    for table in result.tables:
        # print(table.keys())
        assert table.bounding_regions is not None
        page = table.bounding_regions[0].page_number
        pages[page]["tables"].append(table_to_struct(table))
    
    return pages
