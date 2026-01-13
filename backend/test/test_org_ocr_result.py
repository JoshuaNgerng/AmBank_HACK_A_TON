import json

with open('debug.json', 'r') as f:
    result = json.load(f)


def table_to_grid(table):
    # print(table.keys())
    grid = [[None]*table.get('columnCount') for _ in range(table.get('rowCount'))]
    for cell in table.get('cells'):
        grid[cell.get('rowIndex')][cell.get('columnIndex')] = cell.get('content').strip()
    return grid

def table_to_struct(table):
    grid = [[None]*table['columnCount'] for _ in range(table['rowCount'])]
    for cell in table['cells']:
        grid[cell['rowIndex']][cell['columnIndex']] = cell['content'].strip()

    header = tuple(grid[0])   # first row is column header
    return {
        "grid": grid,
        "header": header,
        "columns": table['columnCount']
    }


def gen_pages_info(result):
    pages = {}

    for i in range(len(result.get('pages'))):
        pages[i + 1] = {'text': '', 'tables': []}

    # Text
    for p in result.get('pages'):
        # print(p.keys())
        pages[p.get('pageNumber')]["text"] = "\n".join(l.get("content") for l in p.get('lines'))

    # Tables
    for table in result.get('tables'):
        # print(table.keys())
        page = table.get('boundingRegions')[0].get('pageNumber')
        pages[page]["tables"].append(table_to_struct(table))
    
    return pages

def build_chunks(pages):
    chunks = []
    current = None

    for page_no in sorted(pages.keys()):
        for table in pages[page_no]["tables"]:
            # print(table)
            fp = (table["columns"], table["header"])

            if current and current["fingerprint"] == fp:
                current["tables"].append(table["grid"])
                current["pages"].add(page_no)
            else:
                current = {
                    "fingerprint": fp,
                    "pages": {page_no},
                    "tables": [table["grid"]],
                    "section": None
                }
                chunks.append(current)

    return chunks


def clean_json(obj):
    if isinstance(obj, tuple):
        return [clean_json(x) for x in obj]

    if isinstance(obj, list):
        return [clean_json(x) for x in obj]

    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}
    
    if isinstance(obj, set):
        return list(obj)

    return obj

# def fingerprint(table):
#     headers = []
#     col_positions = []

#     for cell in table.get('cells'):
#         # print(cell)
#         if cell.get('rowIndex') == 0:
#             headers.append(cell.get('content').lower().strip())
#             box = cell.get('boundingRegions')[0].get('polygon')
#             col_positions.append(round(box[0], 1))  # x-start

#     return (
#         table.get('columnCount'),
#         tuple(headers),
#         tuple(col_positions)
#     )


# def similar(fp1, fp2):
#     if fp1 is None or fp2 is None:
#         return False

#     if fp1[0] != fp2[0]:
#         return False

#     header_overlap = len(set(fp1[1]) & set(fp2[1]))
#     if header_overlap >= max(1, len(fp1[1]) // 2):
#         return True

#     pos_diff = sum(abs(a-b) for a,b in zip(fp1[2], fp2[2]))
#     return pos_diff < 1.0

# chunks = []
# # print(result.keys())
# current = {
#     "tables": [],
#     "pages": {},
#     "fingerprint": None
# }
# prev_fp = None
# for table in result.get('tables'):
#     fp = fingerprint(table)
#     if prev_fp and similar(fp, prev_fp):
#         current["tables"].append(table)
#         current["pages"].add(table["boundingRegions"][0]["pageNumber"])
#         if current['fingerprint'] is None:
#             current['fingerprint'] = fp
#     else:
#         current = {
#             "tables": [table],
#             "pages": {table["boundingRegions"][0]["pageNumber"]},
#             "fingerprint": fp
#         }
#         chunks.append(current)

#     prev_fp = fp


pages = gen_pages_info(result)

with open('debug2.json', 'w') as f:
    json.dump(pages, f, indent=4)

# chunks = clean_json(build_chunks(pages))

# with open('debug3.json', 'w') as f:
#     json.dump(chunks, f, indent=4)

# def merge_chunk_tables(chunk):
#     merged = []
#     for t in chunk["tables"]:
#         if not merged:
#             merged = t
#         else:
#             merged.extend(t[1:])   # skip duplicate header
#     return merged

# with open('debug4.json', 'w') as f:
#     json.dump(merge_chunk_tables(chunks), f, indent=4)