import pdfplumber
from docx import Document as DocxDocument

def load_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def load_docx(file_path):
    doc = DocxDocument(file_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text

def load_txt(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def process_document(file_path, file_type):
    if file_type == 'pdf':
        return load_pdf(file_path)
    elif file_type == 'docx':
        return load_docx(file_path)
    elif file_type == 'txt':
        return load_txt(file_path)
    return None

