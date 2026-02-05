from sqlalchemy import String, DateTime, Integer, MetaData, ForeignKey, Numeric, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.models.base import TableBase
from app.models.report import Industry

class NewsInfo(TableBase):
    __tablename__ = "news_info"
    title: Mapped[str] = mapped_column(String)
    summary: Mapped[str] = mapped_column(String)
    published: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    industry: Mapped[Industry] = mapped_column(
        Enum(
            Industry,
            name="industry_enum",
            native_enum=True,     # use PostgreSQL ENUM
            create_constraint=True,
        )
    )

class NewsLink(TableBase):
    __tablename__ = "news_link"

    news_id: Mapped[int] = mapped_column(
        ForeignKey("news_info.id", ondelete="CASCADE"),
        primary_key=True,
    )
    owner_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    revelance: Mapped[float] = mapped_column(Numeric(5, 2))
    news: Mapped["NewsInfo"] = relationship("NewsInfo")
