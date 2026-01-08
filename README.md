# SmartStudy AI

SmartStudy is an AI-powered study assistant that:
- Answers questions using uploaded PDF content
- Falls back to AI-generated answers when content is not found in the PDF
- Avoids repetition and provides clean, readable responses

## Features
- PDF upload and processing
- PDF-based question answering
- AI-based fallback answers
- FastAPI backend
- FAISS vector search

## Tech Stack
- Python
- FastAPI
- FAISS
- Sentence Transformers
- Ollama

## How to Run
```bash
pip install -r requirements.txt
uvicorn app:app --reload
