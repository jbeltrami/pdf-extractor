import fitz  # PyMuPDF
from datetime import datetime

def extract_pages_with_keywords(pdf_path, keywords, output_path):
    doc = fitz.open(pdf_path)

    unique_pages_with_keywords = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()

        for keyword in keywords:
            if keyword.lower() in text.lower():
                if page_num not in unique_pages_with_keywords:
                    unique_pages_with_keywords.append(page_num)

    if unique_pages_with_keywords:
        new_doc = fitz.open()

        # Sort the page numbers to maintain the original order
        unique_pages_with_keywords.sort()

        for page_num in unique_pages_with_keywords:
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

        new_doc.save(output_path)
        new_doc.close()

        print(f'Pages with keywords saved to: {output_path}')
    else:
        print('No pages with keywords found.')

    doc.close()