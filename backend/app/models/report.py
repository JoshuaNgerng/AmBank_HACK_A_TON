from models.base import TableBase
from sqlalchemy.orm import Mapped, mapped_column

class ReportAnalysis(TableBase):
    page_count: Mapped[int] = mapped_column()