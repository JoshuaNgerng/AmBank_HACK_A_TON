import sys
import json
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

# ocr = PaddleOCR(
#     # lang=lang,
#     text_detection_model_name=det_model_name,
#     text_recognition_model_name=rec_model_name,
#     # text_detection_model_name=self.det_model_name,
#     # text_recognition_model_name=self.rec_model_name,
#     use_doc_orientation_classify=False,
#     use_doc_unwarping=False,
#     use_textline_orientation=False,
#     lang='en'
# ) 

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"      # hard disable GPU
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"

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

# def poly_to_bbox(poly):
#     xs = [p[0] for p in poly]
#     ys = [p[1] for p in poly]
#     return min(xs), min(ys), max(xs), max(ys)

# def group_polygon(coor: list[list[int]], text: list[str]):
#     items = []
#     for c, line in zip(coor, text):
#         x1,y1,x2,y2 = poly_to_bbox(c)
#         items.append({
#             "x1": x1, "y1": y1,
#             "x2": x2, "y2": y2,
#             "text": text
#         })
#     return items

# def check_tables(items):
#     items = sorted(items, key=lambda x: x["y1"])

#     rows = []
#     row_threshold = 10   # pixels (tune this)

#     for item in items:
#         placed = False
#         for row in rows:
#             ry1, ry2 = row["y_range"]
            
#             # Check vertical overlap / closeness
#             if abs(item["y1"] - ry1) < row_threshold:
#                 row["cells"].append(item)
#                 row["y_range"] = (
#                     min(ry1, item["y1"]),
#                     max(ry2, item["y2"])
#                 )
#                 placed = True
#                 break
        
#         if not placed:
#             rows.append({
#                 "y_range": (item["y1"], item["y2"]),
#                 "cells": [item]
#             })
#     return rows


with open(sys.argv[1], 'rb') as f:
    data = f.read()

with pdf_open(stream=data) as pdf:
    for page in pdf:
        img = pdf_page_to_cv2_rgb(page)
        # page.number
        # res = ocr.predict(img)
        print(f'checking the predict for {page.number}')
        res = engine.predict(img)
        test = res[0]._to_json()

        with open(f'example_{page.number}.json', 'w') as f:
            json.dump(test, f, indent=2)
        
        if int(page.number or 0) > 3:
            break


        # for i, r in enumerate(res):
        #     # buffer = r._to_json()
        #     print(r.keys())
        #     boxes = group_polygon(r['rec_polys'], r['rec_texts'])
        #     # print(boxes)
        #     buffer = check_tables(boxes)
        #     print(buffer)
        #     with open(f'example_{i}.json', 'w') as f:
        #         json.dump(buffer, f, indent=2)
            # print(r['dt_polys'])
            # for k, v in r.items():
            #     print(f'{k}: {type(v)}')