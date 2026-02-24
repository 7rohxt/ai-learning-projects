import fitz
import pdfplumber

import base64
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4o")

def caption_image(image_bytes):
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    message = HumanMessage(
        content=[
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{b64}"
                }
            },
            {
                "type": "text",
                "text": "Describe this image concisely for a RAG system."
            }
        ]
    )

    response = llm.invoke([message])
    return response.content

def table_to_markdown(table):
    if not table: return ""
    headers = table[0]
    rows = table[1:]
    md = "| " + " | ".join(str(h or "") for h in headers) + " |\n"
    md += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for row in rows:
        md += "| " + " | ".join(str(c or "") for c in row) + " |\n"
    return md

def extract_ordered_content(pdf_path, verbose=True):
    if verbose:
        print(f"\n📂 Opening PDF: {pdf_path}")

    fitz_doc = fitz.open(pdf_path)
    all_content = []

    with pdfplumber.open(pdf_path) as plumber_doc:
        for page_num in range(len(fitz_doc)):
            
            if verbose:
                print(f"\n🔹 Processing Page {page_num + 1}")

            page_blocks = []
            fitz_page = fitz_doc[page_num]
            plumber_page = plumber_doc.pages[page_num]

            tables = plumber_page.find_tables()
            table_bboxes = [t.bbox for t in tables]

            if verbose:
                print(f"   ➤ Tables detected: {len(tables)}")

            def is_inside_table(bbox, table_bboxes):
                for tb in table_bboxes:
                    if bbox[0] >= tb[0] and bbox[1] >= tb[1] and bbox[2] <= tb[2] and bbox[3] <= tb[3]:
                        return True
                return False

            # --- 1. Text blocks ---
            blocks = fitz_page.get_text("dict")["blocks"]
            text_count = 0

            for block in blocks:
                if is_inside_table(block["bbox"], table_bboxes):
                    continue

                if block["type"] == 0:
                    text = " ".join(
                        span["text"] for line in block["lines"] for span in line["spans"]
                    ).strip()

                    if text:
                        text_count += 1
                        page_blocks.append({
                            "type": "text",
                            "content": text,
                            "page": page_num + 1,
                            "y": block["bbox"][1]
                        })

            if verbose:
                print(f"   ➤ Text blocks added: {text_count}")

            # --- 2. Images ---
            images = fitz_page.get_images(full=True)
            if verbose:
                print(f"   ➤ Images detected: {len(images)}")

            for img in images:
                xref = img[0]
                try:
                    img_bbox = fitz_page.get_image_bbox(img)
                    img_data = fitz_doc.extract_image(xref)

                    if verbose:
                        print(f"      ↳ Captioning image xref={xref}")

                    caption = caption_image(img_data["image"])

                    page_blocks.append({
                        "type": "image",
                        "content": f"[IMAGE DESCRIPTION]: {caption}",
                        "page": page_num + 1,
                        "y": img_bbox.y0
                    })

                except Exception as e:
                    print(f"      ⚠ Skipping image xref={xref}: {e}")
                    continue

            # --- 3. Tables ---
            table_count = 0
            for table in tables:
                md = table_to_markdown(table.extract())
                if md:
                    table_count += 1
                    page_blocks.append({
                        "type": "table",
                        "content": f"[TABLE]:\n{md}",
                        "page": page_num + 1,
                        "y": table.bbox[1]
                    })

            if verbose:
                print(f"   ➤ Tables added: {table_count}")

            # --- 4. Sort by y position ---
            page_blocks_sorted = sorted(page_blocks, key=lambda b: b["y"])
            all_content.extend(page_blocks_sorted)

    if verbose:
        print("\n✅ Extraction complete.\n")

    return all_content