import datetime
import sys
import json
from app.core.database import from_dict, get_db_session
from app.models.analysis import GrowthPotential, DegreeLevelEnum
from app.models.report import ReportingPeriod, Company
from app.models.dashboard import CompanyDashboard
from app.services.dashboard import shape_dashboard_info
from app.schemas.dashboard import CompanyAnalysis, CompanyAnalysisResult

from sqlalchemy import select
data = {'growth_level': DegreeLevelEnum.VERY_LOW, 'growth_score': 0.0, 'growth_drivers': '[]', 'constraints': '[]', 'summary': None, 'confidence': 0.1, 'remarks': "No information regarding growth, growth drivers, or constraints was found in the provided text. The section titled 'PROSPECTS' was empty, and other sections did not contain relevant details for growth analysis.", 'reporting_period_id': None, 'created_at': datetime.datetime(2026, 2, 5, 15, 19, 19, 324426), 'updated_at': datetime.datetime(2026, 2, 5, 15, 19, 19, 324433)}

with get_db_session() as db:
    # report = db.execute(
    #     select(ReportingPeriod).where(ReportingPeriod.company_id == 1)
    # ).scalars().first()
    # if report is None:
    #     sys.exit(1)
    # report.growth_potential = from_dict(GrowthPotential, data)
    # db.commit()
    dashboard = db.execute(
        select(CompanyDashboard)
    ).scalars().first()
    company = db.execute(
        select(Company).where(Company.id == dashboard.company_id)
    ).scalar_one_or_none()
    if not dashboard or not company:
        sys.exit(1)
    try:
        check = shape_dashboard_info(company, dashboard)
        with open('debug.json', 'w')as f:
            json.dump(check, f, indent=4)
        res = CompanyAnalysis.model_validate(check)
        # print(res)
        res = CompanyAnalysisResult(
            success=True,
            data=CompanyAnalysis.model_validate(check)
        )
    except Exception as e:
        print(e)
