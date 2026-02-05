from app.services.ai_prompt import get_gemini_client
from app.schemas.company_info import CompanyInfo
from app.models.source import Source
from app.core.logging import logger

def prompt_company_info(text: str) -> CompanyInfo:
    result = get_gemini_client().single_prompt_answer(
        sys_prompt=(
            "You are an assistant that look at extracted text from an annual report, "
            "please fill in the company info according to the schema "
            "if company name or resigtration no cannot be confidently identified set it as NULL"
        ),
        usr_prompt=text,
        response_schema=CompanyInfo
    )
    return result # type: ignore

def get_company_info(sources_list: list[Source]) -> CompanyInfo | None:
    res = ''
    for data in sources_list:
        if data.title:
            res += data.title + '\n'
        if data.body:
            res += data.body + '\n'
        if len(res) > 10000:
            break
    return prompt_company_info(res)

