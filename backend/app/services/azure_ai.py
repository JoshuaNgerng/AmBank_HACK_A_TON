import json
import sys

from openai import AzureOpenAI

from core.config import settings

api_version = "2024-12-01-preview"

model_name = "gpt-5-chat"
deployment = "gpt-5-chat"

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=settings.AZURE_TARGET_URL,
    api_key=settings.AZURE_API_KEY,
)

def single_prompt_answer(sys_prompt: str, usr_prompt: str):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": sys_prompt
            },
            {
                "role": "user",
                "content": usr_prompt
            }
        ],
        max_tokens=16384,
        temperature=0.1,
        top_p=1.0,
        model=deployment
    )

    return response.choices[0].message.content
