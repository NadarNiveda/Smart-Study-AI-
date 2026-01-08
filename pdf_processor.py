# pdf_processor.py

import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader

VECTOR_DIR = "vectorstore"
os.makedirs(VECTOR_DIR, exist_ok=True)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def ingest_pdf(pdf_path: str):

    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    # Chunking (clean & meaningful)
    chunks = [p.strip() for p in text.split("\n") if len(p.strip()) > 40]

    embeddings = embedder.encode(chunks).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, os.path.join(VECTOR_DIR, "index.faiss"))

    with open(os.path.join(VECTOR_DIR, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)
