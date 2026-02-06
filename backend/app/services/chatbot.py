import json
from google import genai
from google.genai import types
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.schemas.ask_bot import UserQuestion
from app.models.report import Company
from app.models.dashboard import CompanyDashboard
from app.services.dashboard import update_dashboard, shape_dashboard_info

client = genai.Client(api_key=settings.GEMINI_API_KEY)

sys_prompt = """
You are a company analysis assistant.
You MUST only use the provided context.
If information is missing, say "This information is not available".
Never speculate.
"""

def build_company_context(company_id: int, db: Session):
    summary = db.execute(
        select(CompanyDashboard).where(CompanyDashboard.company_id == company_id)
    ).scalar_one_or_none()
    company = db.execute(
        select(Company).where(Company.id == company_id)
    ).scalar_one_or_none()
    if not summary or not company: raise ValueError('')
    if not summary.summary or not summary.details:
        update_dashboard(company_id, db)
    buffer = shape_dashboard_info(company, summary)
    return json.dumps(buffer)

def make_conversation(question: UserQuestion, db: Session):
    company_context = ""
    if question.context:
        try:
            company_context = build_company_context(
                question.context.company_id, db
            )
        except:
            return f"Cannot find the company you are refering to"

    sys_prompt = f"""
You are a company assistant.
Use ONLY the following company information.

{company_context}
"""

    history = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=m)]
        )
        for m in question.chat_history
    ]


    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=sys_prompt,
            temperature=0.2
        ),
        history=history # type: ignore
    )

    return "".join(
        chunk.text or ""
        for chunk in chat.send_message_stream(question.message)
    )

