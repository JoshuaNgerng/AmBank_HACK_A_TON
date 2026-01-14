from models.base import Base
from core.database import engine, get_db
from fastapi import APIRouter, Depends
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

def init_db():
    # This creates all tables defined in models that inherit from Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

router = APIRouter()

@router.get('/init_db')
async def admin_init_db(db: Session = Depends(get_db)):
    try:
        init_db()
    except:
        return "FAK UP"
    return "DB init success"

@router.get('/clear_db')
async def admin_clear_db(db: Session = Depends(get_db)):
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)

    return "DB cleared"