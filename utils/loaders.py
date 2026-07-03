import os
import pandas as pd

from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from langchain_core.documents import Document


# ==========================================================
# PDF Loader
# ==========================================================

def load_pdf(file_path):

    documents = []

    reader = PdfReader(file_path)

    for page_no, page in enumerate(reader.pages):

        text = page.extract_text()

        if text:

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": os.path.basename(file_path),
                        "file_type": "PDF",
                        "page": page_no + 1
                    }
                )
            )

    return documents


# ==========================================================
# DOCX Loader
# ==========================================================

def load_docx(file_path):

    documents = []

    doc = DocxDocument(file_path)

    text = "\n".join(
        para.text
        for para in doc.paragraphs
        if para.text.strip()
    )

    documents.append(
        Document(
            page_content=text,
            metadata={
                "source": os.path.basename(file_path),
                "file_type": "DOCX"
            }
        )
    )

    return documents


# ==========================================================
# TXT Loader
# ==========================================================

def load_txt(file_path):

    documents = []

    with open(file_path, "r", encoding="utf-8") as f:

        text = f.read()

    documents.append(
        Document(
            page_content=text,
            metadata={
                "source": os.path.basename(file_path),
                "file_type": "TXT"
            }
        )
    )

    return documents


# ==========================================================
# CSV Loader
# ==========================================================

def load_csv(file_path):

    documents = []

    df = pd.read_csv(file_path)

    for _, row in df.iterrows():

        text = "\n".join(
            f"{col}: {row[col]}"
            for col in df.columns
        )

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": os.path.basename(file_path),
                    "file_type": "CSV"
                }
            )
        )

    return documents


# ==========================================================
# Markdown Loader
# ==========================================================

def load_md(file_path):

    documents = []

    with open(file_path, "r", encoding="utf-8") as f:

        text = f.read()

    documents.append(
        Document(
            page_content=text,
            metadata={
                "source": os.path.basename(file_path),
                "file_type": "Markdown"
            }
        )
    )

    return documents


# ==========================================================
# Main Loader
# ==========================================================

def load_documents(folder="knowledge"):

    documents = []

    supported_files = {
        ".pdf": load_pdf,
        ".docx": load_docx,
        ".txt": load_txt,
        ".csv": load_csv,
        ".md": load_md
    }

    for file in os.listdir(folder):

        file_path = os.path.join(folder, file)

        extension = os.path.splitext(file)[1].lower()

        loader = supported_files.get(extension)

        if loader:

            try:

                documents.extend(loader(file_path))

            except Exception as e:

                print(f"Error loading {file}: {e}")

    return documents