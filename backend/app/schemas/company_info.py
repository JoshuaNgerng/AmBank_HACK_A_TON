from pydantic import BaseModel

class CompanyInfo(BaseModel):
    company_name: str | None
    resigtration_no: str | None
