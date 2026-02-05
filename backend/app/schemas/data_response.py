from pydantic import BaseModel

class ReportProcessingStatus(BaseModel):
    status: str

class IncompleteTasks(BaseModel):
    task_id: int
    celery_task_id: str
    report_id: int
    file_key: str