import fitz
import sys

doc = fitz.open(sys.argv[1])
print(doc.page_count)

for i in range(doc.page_count):
    print(i, doc.load_page(i).get_text()[:50])
