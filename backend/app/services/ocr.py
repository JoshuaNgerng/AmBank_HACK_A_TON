import fitz  # PyMuPDF
from fitz import Document
import pytesseract
from PIL import Image
import io

def extract_page_text(page):
    # Try digital text extraction
    text = page.get_text()
    if text.strip():
        return text

    # Fallback: render page as image for OCR
    pix = page.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    text = pytesseract.image_to_string(img, lang='eng')
    return text

def ocr_annual_report_with_fitz(doc: Document):
    all_pages_text = []

    for page_number, page in enumerate(doc, start=1):
        raw_text = extract_page_text(page)
        all_pages_text.append({
            "page_number": page_number,
            "raw_text": raw_text
        })

    return all_pages_text
