from typing import Any, TYPE_CHECKING, ClassVar
from decimal import Decimal
from datetime import datetime
from enum import Enum as ENUM
from sqlalchemy import (
    Integer, String, Float, Boolean, Numeric, 
    Enum, ForeignKey,  ARRAY,inspect
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign 
from sqlalchemy.ext.declarative import declared_attr
from app.models.base import TableBase

if TYPE_CHECKING:
    from app.models.report import CompanyReport, ReportingPeriod

class PossibleSignal(ENUM):
    business_strategy  = "business_strategy"
    growth_potential = "growth_potential"
    risk_analysis  = "risk_analysis" 
    qualitative_performance  = "qualitative_performance"

class PossibleStatement(ENUM):
    income_statement = "income_statement"
    balance_sheet = "balance_sheet"
    cash_flow_statement = "cash_flow_statement"

class Source(TableBase):
    __tablename__ = "source"

    page_number: Mapped[int] = mapped_column(Integer)
    statement_type: Mapped[PossibleStatement | None] = mapped_column(
        Enum(
            PossibleStatement,
            name="statement_type_enum",
            native_enum=True,     # use PostgreSQL ENUM
            create_constraint=True,
        ),
        nullable=True,
    )
    signals: Mapped[list[PossibleSignal]] = mapped_column(
        ARRAY(
            Enum(
                PossibleSignal,
                name="possible_signal_enum",
                native_enum=True,
                create_constraint=True
            )
        ),
        nullable=False,
        default=list  
    )
    title: Mapped[str] = mapped_column(String)
    body: Mapped[str] = mapped_column(String)
    tables: Mapped[str] = mapped_column(String)
    classification_remarks = mapped_column(String)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)

    report_id: Mapped[int] = mapped_column(ForeignKey("company_report.id"))
    company_report: Mapped["CompanyReport"] = relationship(
        back_populates="report_sources", uselist=False,
    )
    is_from_lastest_report: Mapped[bool] = mapped_column(Boolean, default=False)

class SourceLink(TableBase):
    __tablename__ = "source_link"

    source_id: Mapped[int] = mapped_column(
        ForeignKey("source.id", ondelete="CASCADE"),
        primary_key=True,
    )

    owner_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_type: Mapped[str] = mapped_column(String, primary_key=True, index=True)

    source: Mapped["Source"] = relationship("Source")

class SourceLinker(TableBase):
    """
    Mixin that adds a polymorphic 'sources' relationship
    and helper method to link sources automatically.
    """

    __abstract__ = True
    _sources_cache: ClassVar[list["Source"] | None] = None

    @declared_attr
    def source_links(cls) -> Mapped[list["SourceLink"]]:
        return relationship(
            "SourceLink",
            primaryjoin=lambda: (
                (cls.id == foreign(SourceLink.owner_id)) &
                (SourceLink.owner_type == cls.__tablename__)
            ),
            cascade="all, delete-orphan",
            single_parent=True,
            overlaps="source_links"
        )

    def get_sources(self) -> list["Source"]:
        """
        Return sources linked to this object.

        This method is SAFE for async usage:
        - It never triggers lazy loading
        - It raises if required relationships are not eagerly loaded
        - Results are cached after first call
        """

        # Return cached result if available
        if self._sources_cache is not None:
            return self._sources_cache

        state = inspect(self)

        # 1️⃣ Ensure source_links is loaded
        if not state.attrs.source_links.loaded:
            raise RuntimeError(
                f"{self.__class__.__name__}.source_links is not loaded.\n"
                f"Use eager loading:\n"
                f"  selectinload({self.__class__.__name__}.source_links)"
                f".selectinload(SourceLink.source)"
            )

        sources: list["Source"] = []

        # 2️⃣ Ensure each SourceLink.source is loaded
        for link in self.source_links:
            link_state = inspect(link)
            if not link_state.attrs.source.loaded:
                raise RuntimeError(
                    f"SourceLink.source is not loaded.\n"
                    f"Use eager loading:\n"
                    f"  selectinload({self.__class__.__name__}.source_links)"
                    f".selectinload(SourceLink.source)"
                )
            sources.append(link.source)

        # 3️⃣ Cache result
        self._sources_cache = sources #type: ignore it just works Kappa
        return sources

    def add_source(self, source: Source | int):
        buffer =  SourceLink(
            owner_type=self.__tablename__
        )
        if isinstance(source, int):
            buffer.source_id = source
        else:
            buffer.source = source
        self.source_links.append(buffer)


class FinicialElementBase(SourceLinker):
    __abstract__ = True
    confidence: Mapped[Decimal] = mapped_column(Numeric(4, 2), default=0.0)
    remarks: Mapped[str | None] = mapped_column(String, default=None, nullable=True)
    reporting_period_id: Mapped[int] = mapped_column(
        ForeignKey("reporting_period.id"), unique=True   # enforces one-to-one in DB
    )
    @declared_attr
    def reporting_period(cls) -> Mapped["ReportingPeriod"]:
        return relationship(back_populates=cls.__tablename__)
