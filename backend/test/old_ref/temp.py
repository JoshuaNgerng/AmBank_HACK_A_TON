import fitz
import pytesseract
from PIL import Image
import io

def detect_statement_from_text(text):
    t = text.lower()

    if "cash flows" in t and "operating activities" in t:
        return "cashflow"
    if "total assets" in t and "total liabilities" in t:
        return "balance"
    if "revenue" in t and "net income" in t:
        return "income"
    if "notes to the financial statements" in t:
        return "notes"

    return "other"


def detect_statement_from_header(header):
    h = " ".join(header).lower()

    if "assets" in h and "liabilities" in h:
        return "balance"
    if "cash flow" in h or "cash flows" in h:
        return "cashflow"
    if "revenue" in h or "net income" in h:
        return "income"

    return None


def extract_page_text(page):
    # Try digital text first
    text = page.get_text()
    if text and text.strip():
        return text, "digital"

    # Fallback to OCR
    pix = page.get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    text = pytesseract.image_to_string(img, lang="eng")
    return text, "ocr"


def get_table_header(text):
    """
    Extract first few table row labels.
    Used to detect table continuation.
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    header = []
    for line in lines[:8]:
        if any(c.isdigit() for c in line):
            break
        header.append(line.lower())
    return tuple(header)


def extract_rows(text):
    rows = []

    for line in text.split("\n"):
        parts = line.split()
        if len(parts) < 2:
            continue

        try:
            value = float(parts[-1].replace(",", "").replace("(", "-").replace(")", ""))
            label = " ".join(parts[:-1])
            rows.append({"line_item": label, "value": value})
        except:
            continue

    return rows

def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    pages = []
    current_table_id = 0
    prev_header = None
    prev_statement = None

    for i, page in enumerate(doc):
        text, source = extract_page_text(page)
        header = get_table_header(text)
        rows = extract_rows(text)

        # Detect table continuation
        if header == prev_header:
            table_id = current_table_id
            statement = prev_statement
        else:
            current_table_id += 1
            table_id = current_table_id
            prev_header = header

            # Detect statement type
            statement = (
                detect_statement_from_header(header)
                or detect_statement_from_text(text)
            )
            prev_statement = statement

        pages.append({
            "page_number": i + 1,
            "table_id": table_id,
            "statement_type": statement,
            "source": source,
            "raw_text": text,
            "rows": rows
        })

    return pages

if __name__ == "__main__":
    import sys
    import json
    res = process_pdf(sys.argv[1])
    with open('result.json', 'w') as f:
        json.dump(res, f, indent=4)
    for i, r in enumerate(res):
        with open(f'{i}.txt', 'w') as f:
            f.write(r['raw_text'])