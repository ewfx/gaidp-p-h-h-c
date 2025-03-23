import os
from PyPDF2 import PdfReader

def extract_pdf_text(file_path, pages_to_load, output_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist. Please check the path.")

    pdf = PdfReader(file_path)
    raw_text = ""

    for page_num in pages_to_load:
        if page_num < len(pdf.pages):
            content = pdf.pages[page_num].extract_text()
            if content:
                raw_text += f"\n--- Page {page_num + 1} ---\n{content}"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(raw_text)

    print(f"Text extraction completed. Output saved to {output_path}")