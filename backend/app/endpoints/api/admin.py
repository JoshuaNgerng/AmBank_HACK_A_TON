from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from app.models.base import Base
from app.core.database import engine, get_db

def init_db():
    # This creates all tables defined in models that inherit from Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

router = APIRouter()

@router.get('/init_db')
async def admin_init_db(db: Session = Depends(get_db)):
    try:
        init_db()
    except Exception as e:
        return f"FAK UP: {e}"
    return "DB init success"

@router.get('/clear_db')
async def admin_clear_db(db: Session = Depends(get_db)):
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)

    return "DB cleared"

@router.get('/check_db_models')
async def admin_get_sht(db: Session = Depends(get_db)):
    from app.models.report import Company, CompanyReport, ReportingPeriod
    from app.models.source import Source, SourceLink
    from app.models.statements import IncomeStatement, CashFlowStatement, BalanceSheet
    from app.models.analysis import QualitativePerformance, BusinessStrategy, RiskAnalysis, GrowthPotential

    try:
        test = Company()
        print('company')
        test = CompanyReport()
        print('companyreport')
        test = ReportingPeriod()
        print('reporintperiod')
        test = Source()
        print('source')
        test = SourceLink()
        print('source link')
        test = IncomeStatement()
        print('income ')
        test = CashFlowStatement()
        print('cash')
        test = BalanceSheet()
        print('balance')
        test = QualitativePerformance()
        print('perform')
        test = BusinessStrategy()
        print('strats')
        test = RiskAnalysis()
        print('risk')
        test = GrowthPotential()
        print('growth')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return "Init all db model orm successful"