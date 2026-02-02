from app.services.ai_prompt import get_gemini_client
from app.schemas.classify import TextSection
from app.schemas.company_info import CompanyInfo
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

def get_company_info(ocr_result: list[list[TextSection]]) -> CompanyInfo:
    res = ''
    for line in ocr_result:
        # logger.info(type(line))
        for data in line:
            # logger.info(f'debug get company info loop: {type(data)}')
            res += data.content + '\n'
            if len(res) > 10000:
                break
        if len(res) > 10000:
            break
    return prompt_company_info(res)

