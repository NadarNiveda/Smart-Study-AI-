# app.py

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os
import shutil

from qa_engine import answer_question
from pdf_processor import ingest_pdf

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class QuestionRequest(BaseModel):
    question: str

@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):

    pdf_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_pdf(pdf_path)

    return {"message": "PDF uploaded and indexed successfully"}

@app.post("/ask")
def ask_question(q: QuestionRequest):

    answer = answer_question(q.question)
    return {"answer": answer}
