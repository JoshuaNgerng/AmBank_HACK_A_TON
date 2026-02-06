from typing import Any, TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy import Integer, String, Enum, ForeignKey, Float, DateTime, ARRAY, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from app.models.base import TableBase
from enum import Enum as ENUM

if TYPE_CHECKING:
    from app.models.statements import IncomeStatement, BalanceSheet, CashFlowStatement
    from app.models.analysis import BusinessStrategy, RiskAnalysis, QualitativePerformance, GrowthPotential
    from app.models.source import Source, PossibleStatement, PossibleSignal
    from app.models.dashboard import CompanyDashboard

class Industry(ENUM):
    # Primary industries
    AGRICULTURE = "agriculture"
    FORESTRY = "forestry"
    FISHING = "fishing"
    MINING = "mining"
    OIL_AND_GAS = "oil_and_gas"

    # Manufacturing & industrial
    MANUFACTURING = "manufacturing"
    INDUSTRIALS = "industrials"
    CHEMICALS = "chemicals"
    METALS = "metals"
    AUTOMOTIVE = "automotive"
    AEROSPACE_DEFENSE = "aerospace_defense"
    ELECTRONICS = "electronics"
    SEMICONDUCTORS = "semiconductors"

    # Energy & utilities
    ENERGY = "energy"
    RENEWABLE_ENERGY = "renewable_energy"
    UTILITIES = "utilities"
    WATER_AND_WASTE = "water_and_waste"

    # Construction & real assets
    CONSTRUCTION = "construction"
    REAL_ESTATE = "real_estate"
    INFRASTRUCTURE = "infrastructure"

    # Consumer-facing
    RETAIL = "retail"
    WHOLESALE = "wholesale"
    ECOMMERCE = "ecommerce"
    CONSUMER_GOODS = "consumer_goods"
    FOOD_AND_BEVERAGE = "food_and_beverage"
    HOSPITALITY = "hospitality"
    TRAVEL_AND_TOURISM = "travel_and_tourism"
    ENTERTAINMENT = "entertainment"
    MEDIA = "media"
    GAMING = "gaming"
    SPORTS = "sports"
    FASHION_AND_APPAREL = "fashion_and_apparel"
    LUXURY_GOODS = "luxury_goods"

    # Technology
    TECHNOLOGY = "technology"
    SOFTWARE = "software"
    HARDWARE = "hardware"
    INFORMATION_TECHNOLOGY = "information_technology"
    ARTIFICIAL_INTELLIGENCE = "artificial_intelligence"
    DATA_AND_ANALYTICS = "data_and_analytics"
    CLOUD_COMPUTING = "cloud_computing"
    CYBERSECURITY = "cybersecurity"
    BLOCKCHAIN_AND_WEB3 = "blockchain_and_web3"
    INTERNET_SERVICES = "internet_services"
    TELECOMMUNICATIONS = "telecommunications"

    # Healthcare & life sciences
    HEALTHCARE = "healthcare"
    BIOTECHNOLOGY = "biotechnology"
    PHARMACEUTICALS = "pharmaceuticals"
    MEDICAL_DEVICES = "medical_devices"
    DIGITAL_HEALTH = "digital_health"
    HEALTH_INSURANCE = "health_insurance"

    # Financial & professional services
    FINANCIAL_SERVICES = "financial_services"
    BANKING = "banking"
    INSURANCE = "insurance"
    INVESTMENT_MANAGEMENT = "investment_management"
    FINTECH = "fintech"
    ACCOUNTING = "accounting"
    LEGAL_SERVICES = "legal_services"
    CONSULTING = "consulting"
    PROFESSIONAL_SERVICES = "professional_services"

    # Education & research
    EDUCATION = "education"
    E_LEARNING = "e_learning"
    RESEARCH_AND_DEVELOPMENT = "research_and_development"

    # Transportation & logistics
    TRANSPORTATION = "transportation"
    LOGISTICS = "logistics"
    SHIPPING = "shipping"
    AVIATION = "aviation"
    RAIL = "rail"
    AUTOMOTIVE_SERVICES = "automotive_services"

    # Public & social sectors
    GOVERNMENT = "government"
    PUBLIC_ADMINISTRATION = "public_administration"
    NON_PROFIT = "non_profit"
    SOCIAL_ENTERPRISE = "social_enterprise"

    # Environment & sustainability
    ENVIRONMENTAL_SERVICES = "environmental_services"
    CLIMATE_TECH = "climate_tech"
    SUSTAINABILITY = "sustainability"
    RECYCLING = "recycling"

    # Other / fallback
    HUMAN_RESOURCES = "human_resources"
    SECURITY_SERVICES = "security_services"
    FACILITIES_MANAGEMENT = "facilities_management"
    OTHER = "other"

class ReportingPeriod(TableBase):
    __tablename__ = "reporting_period"

    # must be the same as the CompanyReport its from never change it after creation
    report_date: Mapped[datetime] = mapped_column(DateTime)
    # e.g. 2024, 2023, "5_year_summary", "historical"
    period_label: Mapped[str] = mapped_column(String)
    fiscal_year: Mapped[int] = mapped_column(Integer)
    period_type: Mapped[str] = mapped_column(String)
    # "annual", "historical_summary", "quarterly", "unknown"

    # Finicial Statements
    income_statement: Mapped["IncomeStatement"] = relationship(
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )

    balance_sheet: Mapped["BalanceSheet"] = relationship(
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )

    cash_flow_statement: Mapped["CashFlowStatement"] = relationship(
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Finicial Analysis

    business_strategy: Mapped["BusinessStrategy"] = relationship(
        "BusinessStrategy",
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )

    risk_analysis: Mapped["RiskAnalysis"] = relationship(
        "RiskAnalysis",
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )

    qualitative_performance: Mapped["QualitativePerformance"] = relationship(
        "QualitativePerformance",
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )

    growth_potential: Mapped["GrowthPotential"] = relationship(
        "GrowthPotential",
        back_populates="reporting_period",
        uselist=False,
        cascade="all, delete-orphan"
    )
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company: Mapped["Company"] = relationship(
        back_populates="reporting_period",
        uselist=False,
    )

class CompanyReport(TableBase):
    __tablename__ = "company_report"

    file_key: Mapped[str] = mapped_column(String, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    celery_task_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    report_type: Mapped[str | None] = mapped_column(String, nullable=True)
    # "annual", "quarterly", "prospectus", etc.
    report_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_pages: Mapped[int] = mapped_column(Integer, default=0)

    company_id: Mapped[int | None] = mapped_column(ForeignKey("company.id"), nullable=True)
    company: Mapped["Company"] = relationship(back_populates="company_reports")

    report_sources: Mapped[list["Source"]] = relationship(
        back_populates="company_report",
        cascade="all, delete-orphan"
    )

class Company(TableBase):
    __tablename__ = "company"

    company_id: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)  
    # ticker, registration number, etc.
    company_name: Mapped[str | None] = mapped_column(String(200), nullable=True)

    industry: Mapped[Industry | None] = mapped_column(
        Enum(
            Industry,
            name="industry_enum",
            native_enum=True,     # use PostgreSQL ENUM
            create_constraint=True,
        ),
        nullable=True
    )

    company_reports: Mapped[list["CompanyReport"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )
    reporting_period: Mapped[list["ReportingPeriod"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan"
    )

    company_dashboard: Mapped['CompanyDashboard'] = relationship(
        "CompanyDashboard", uselist=False, back_populates="company"
    )

    def get_report_by_year(self, year: int) -> Optional["ReportingPeriod"]:
        for report in self.reporting_period:
            if report.fiscal_year == year:
                return report
        return None