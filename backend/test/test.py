import fitz  # PyMuPDF
import numpy as np
from PIL import Image
import io

def pdf_bytes_to_images(pdf_bytes, dpi=300):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []

    zoom = dpi / 72  # 72 DPI is PDF base
    mat = fitz.Matrix(zoom, zoom)

    for page in doc:
        pix = page.get_pixmap(matrix=mat, alpha=False)

        img = Image.open(io.BytesIO(pix.tobytes("png")))
        img_np = np.array(img)

        images.append(img_np)

    return images

from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_angle_cls=False,
    lang="en",
    # use_gpu=False
)

import re

def classify_page(lines):
    text = " ".join(lines).lower()

    income_keywords = [
        "income statement", "profit and loss", "revenue", "net income",
        "operating income", "earnings"
    ]

    balance_keywords = [
        "balance sheet", "assets", "liabilities", "equity",
        "shareholders", "total assets"
    ]

    cashflow_keywords = [
        "cash flow", "operating activities", "investing activities",
        "financing activities", "net cash"
    ]

    def score(keywords):
        return sum(1 for k in keywords if re.search(k, text))

    scores = {
        "income": score(income_keywords),
        "balance": score(balance_keywords),
        "cashflow": score(cashflow_keywords)
    }

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "other"
    return best

def extract_table(ocr_result):
    rows = []
    for line in ocr_result[0]:
        box = line[0]
        text = line[1][0]
        y_center = (box[0][1] + box[2][1]) / 2
        rows.append((y_center, text))

    rows.sort()

    table = []
    current_row = []
    last_y = None

    for y, text in rows:
        if last_y and abs(y - last_y) > 15:
            table.append(current_row)
            current_row = []
        current_row.append(text)
        last_y = y

    table.append(current_row)
    return table

import pandas as pd

def ocr_report(pdf_bytes):

    results = {
        "income": [],
        "balance": [],
        "cashflow": [],
        "other": []
    }

    pages = pdf_bytes_to_images(pdf_bytes)

    for i, page in enumerate(pages):
        print(f'debuging page {i}')
        ocr_result = ocr.ocr(page)
        lines = [l[1][0] for l in ocr_result[0]]

        page_type = classify_page(lines)
        print(page, "→", page_type)

        if page_type != "other":
            table = extract_table(ocr_result)
            results[page_type].append(table)
    
    return results

if __name__ == "__main__":
    pass
    import sys
    with open(sys.argv[1], 'rb') as f:
        pdf_bytes = f.read()
    res = ocr_report(pdf_bytes)
    print(res)