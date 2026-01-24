import sys
import json
from turtle import title
from paddleocr import PaddleOCR, PPStructureV3
import cv2
import numpy as np
from pymupdf import Page, Matrix, open as pdf_open
from pymupdf.utils import get_pixmap

def preprocess_pdf_page(pdf_page: Page, scale: int = 2) -> np.ndarray:
    pix = get_pixmap(pdf_page, matrix=Matrix(scale, scale))
    im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    im = np.ascontiguousarray(im[..., [2, 1, 0]])  # rgb to bgr
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

def pdf_page_to_cv2_rgb(pdf_page: Page, scale: int = 2):
    bgr = preprocess_pdf_page(pdf_page, scale)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"      # hard disable GPU
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"

loaded: bool = False
det_model_name = 'PP-OCRv5_mobile_det'
rec_model_name = 'en_PP-OCRv5_mobile_rec'
layout_model_name = "PP-DocLayoutV2"
t = [
    "PP-DocLayoutV2",
    "PP-DocLayout-L",
    "PP-DocLayout-M",
    "PP-DocLayout-S",
    "PP-DocLayout_plus-L",
    "PP-DocBlockLayout"
]

from paddleocr import PPStructureV3

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

    lang="en",
)

from enum import StrEnum, auto
from pydantic import BaseModel

class SectionTypes(StrEnum):
    text = auto()
    doc_title = auto()
    paragraph_title = auto()
    table = auto()

class TextSection(BaseModel):
    type: SectionTypes = SectionTypes.text
    confidence: float = 0.0
    content: str = ''

class TextGroup(BaseModel):
    title: str | None
    content: str | None


def extract_text_section(parsing_res_list: list, boxes: list[dict]) -> list[TextSection]:
    res = []
    for p, b in zip(parsing_res_list, boxes):
        type_ = p.label
        if type_ not in SectionTypes:
            continue
        buffer = TextSection(type=type_, confidence=b['score'], content=p.content)
        res.append(buffer)
    return res


def group_sections(text_sections: list[TextSection]) -> list[dict[str, str]]:
    res = []
    buffer = {"title": [], "body": [], "table": []}
    block = False
    for section in text_sections:
        type_ = section.type
        content = section.content
        if type_ == SectionTypes.doc_title or type_ == SectionTypes.paragraph_title:
            if block == True:
                res.append(buffer)
                buffer = {"title": [content], "body": [], "table": []}
                block = False
            else:
                buffer['title'].append(content)
            continue
        if type_ == SectionTypes.table:
            buffer['table'].append(content)
            continue
        buffer['body'].append(content)
    if buffer:
        res.append(buffer)
    return res

if __name__ == "__main__":

    with open(sys.argv[1], 'rb') as f:
        data = f.read()

    with pdf_open(stream=data) as pdf:
        for page in pdf:
            img = pdf_page_to_cv2_rgb(page)
            # page.number
            # res = ocr.predict(img)
            print(f'checking the predict for {page.number}')
            res = engine.predict(img)

            section_list = extract_text_section(res[0]['parsing_res_list'], res[0]['layout_det_res']['boxes'])
            check = group_sections(section_list)
            print(len(check))
            with open(f'debug_section_{page.number}.json', 'w') as f:
                json.dump(check, f, indent=2)
            # buffer = [s.model_dump() for s in section_list]

            # with open(f'example_{page.number}_buffer.json', 'w') as f:
            #     json.dump(buffer, f, indent=2)

            # test = res[0]._to_json()
            # with open(f'example_{page.number}.json', 'w') as f:
            #     json.dump(test, f, indent=2)
            


            if int(page.number or 0) > 3:
                break