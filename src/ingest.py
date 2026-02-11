# src/ingest.py

import os
from typing import List, Dict

from pypdf import PdfReader

def load_documents(folder_path: str):
    documents = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # TXT files
        if filename.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    documents.append({
                        "content": text,
                        "source": filename
                    })

        # PDF files
        elif filename.lower().endswith(".pdf"):
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

            text = text.strip()
            if text:
                documents.append({
                    "content": text,
                    "source": filename
                })

    return documents
