import json
from venv import logger

from core.config import settings

from pydantic import BaseModel
from google import genai
from google.genai import types

# Configure Gemini
client = genai.Client(api_key=settings.GEMINI_API_KEY)

def single_prompt_answer(sys_prompt: str, usr_prompt: str, response_schema: type[BaseModel] | None = None):
    logger.info(f'sys prompt: {sys_prompt}')
    logger.info(f'user prompt: {usr_prompt}')
    response_mime_type = None if not response_schema else "application/json"
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=types.Part.from_text(text=usr_prompt),
            config=types.GenerateContentConfig(
                system_instruction=sys_prompt,
                response_schema=response_schema,
                response_mime_type=response_mime_type,
                temperature=0,
                top_p=0.95,
                top_k=20,
            ),
        )
    except Exception as e:
        logger.error(f'AI cannot process: {e}') 
        return None

    return response.text
