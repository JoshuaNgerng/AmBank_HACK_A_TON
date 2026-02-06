import sys
import json
from copy import deepcopy
from paddleocr import  PPStructureV3
import cv2
import numpy as np
from pymupdf import Document, Page, Matrix, open as pdf_open
from pymupdf.utils import get_pixmap
from app.core.logging import logger
from app.schemas.classify import SectionTypes, TextSection


import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"      # hard disable GPU
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"

loaded: bool = False
det_model_name = 'PP-OCRv5_mobile_det'
rec_model_name = 'en_PP-OCRv5_mobile_rec'
layout_model_name = "PP-DocLayoutV2"

from paddleocr import PPStructureV3

engine = None 


def get_ocr_engine():
    global engine
    if engine: return engine
    engine = PPStructureV3(

        # Layout / region detection (to find table blocks)
        use_region_detection=True,
        layout_detection_model_name=layout_model_name,
        text_detection_model_name=det_model_name,
        text_recognition_model_name=rec_model_name,


        # Table recognition only
        use_table_recognition=True,

        # Disable everything else
        use_chart_recognition=False,
        use_formula_recognition=False,
        use_seal_recognition=False,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        enable_mkldnn=False
        # device="CPU",

        # lang="en",
    )
    return engine

def extract_text_section(parsing_res_list: list, boxes: list[dict]) -> list[TextSection]:
    res = []
    for p, b in zip(parsing_res_list, boxes):
        try:
            type_ = SectionTypes(p.label)
        except:
            type_ = None
        if type_ is None:
            continue
        if type_ not in SectionTypes:
            continue
        buffer = TextSection(type=type_, confidence=b['score'], content=p.content)
        res.append(buffer)
    return res


def preprocess_pdf_page(pdf_page: Page, scale: int = 2) -> np.ndarray:
    pix = get_pixmap(pdf_page, matrix=Matrix(scale, scale))
    im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n).copy()
    im = np.ascontiguousarray(im[..., [2, 1, 0]]).copy()  # rgb to bgr
    return im

def pdf_page_to_bgr(pdf_page: Page, scale: int = 2):
    im = preprocess_pdf_page(pdf_page, scale)
    print(f"debug shape: {im.shape}, type {im.dtype}, flag: {im.flags['C_CONTIGUOUS']}")
    if im.shape[2] == 4:
        im = im[:, :, :3]  # drop alpha
        print('trigger drop alpha')
    elif im.shape[2] == 1:
        im = np.repeat(im, 3, axis=2)  # expand grayscale
        print('trigger expand grayscale')
    return im

def ocr_pdf_report(data: bytes) -> tuple[list[list[TextSection]], int]:
    res : list[list[TextSection]] = []
    engine = get_ocr_engine()
    with pdf_open(stream=data) as pdf:
        count = pdf.page_count
        for page in pdf:
            bgr = preprocess_pdf_page(page)
            img = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            print(f'checking the predict for {page.number}')
            ocr = engine.predict(img)
            # print(res[0]['parsing_res_list'])
            section_list = extract_text_section(ocr[0]['parsing_res_list'], ocr[0]['layout_det_res']['boxes'])
            # for b in section_list:
            #     print(b)
            res.append(section_list)

    return (res, int(count))
