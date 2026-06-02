import os
from PyPDF2 import PdfReader
from docx import Document

def load_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return text

def load_docx(file_path):
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
    return text

def load_txt(file_path):
    text = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading TXT {file_path}: {e}")
    return text

def load_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return load_pdf(file_path)
    elif ext == '.docx':
        return load_docx(file_path)
    elif ext == '.txt':
        return load_txt(file_path)
    else:
        print(f"Unsupported file format: {ext}")
        return ""

def load_documents_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            text = load_document(filepath)
            if text:
                documents.append({"filename": filename, "content": text})
                print(f"Loaded {filename}")
    return documents

if __name__ == "__main__":
    docs = load_documents_from_folder("docs")
    print(f"\nTotal documents loaded: {len(docs)}")