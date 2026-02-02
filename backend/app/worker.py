import paddle
import os

# Hard limits (environment-level)
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["CPU_NUM_THREADS"] = "1"


from app.core.celery import celery_app
import app.celery.ocr
from app.services.ocr import get_ocr_engine

get_ocr_engine()