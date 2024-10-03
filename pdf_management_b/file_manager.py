import json
import os

def save_pdf(filename, title):
    pdf_data = {
        'filename': filename,
        'title': title,
        'upload_date': str(datetime.now())
    }
    pdfs = load_pdfs()
    pdfs.append(pdf_data)
    with open('pdfs.json', 'w') as file:
        json.dump(pdfs, file)

def load_pdfs():
    if os.path.exists('pdfs.json'):
        with open('pdfs.json', 'r') as file:
            return json.load(file)
    return []

def list_pdfs():
    return load_pdfs()

def get_pdf_metadata(filename):
    pdfs = load_pdfs()
    for pdf in pdfs:
        if pdf['filename'] == filename:
            return pdf
    return None