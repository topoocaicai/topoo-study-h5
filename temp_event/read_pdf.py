import pdfplumber

import glob, os
pdf_dir = r'E:\20251001\2025813'
pdf_files = glob.glob(os.path.join(pdf_dir, '*紫金杯*'))
if not pdf_files:
    pdf_files = glob.glob(os.path.join(pdf_dir, '*直播大赛*'))
pdf_path = pdf_files[0] if pdf_files else ''
print(f'Opening: {pdf_path}')
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            print(f'--- Page {i+1} ---')
            print(text)
            print()
