import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
import ollama

VECTOR_DIR = "vectorstore"
INDEX_PATH = os.path.join(VECTOR_DIR, "index.faiss")
CHUNKS_PATH = os.path.join(VECTOR_DIR, "chunks.pkl")

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# --------------------------------------------------
# Utility
# --------------------------------------------------

def pdf_exists() -> bool:
    return os.path.exists(INDEX_PATH) and os.path.exists(CHUNKS_PATH)

def load_store():
    index = faiss.read_index(INDEX_PATH)
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    return index, chunks

def clean_repetition(text: str) -> str:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    seen = set()
    final = []
    for line in lines:
        key = line.lower()
        if key not in seen:
            final.append(line)
            seen.add(key)
    return "\n".join(final)

# --------------------------------------------------
# Main QA Logic
# --------------------------------------------------

def answer_question(question: str) -> str:

    # ============================================
    # CASE 1: PDF EXISTS
    # ============================================
    if pdf_exists():

        index, chunks = load_store()
        q_embedding = embedder.encode([question]).astype("float32")

        distances, indices = index.search(q_embedding, k=6)
        similarities = 1 / (1 + distances[0])

        RELEVANCE_THRESHOLD = 0.50

        relevant_chunks = [
            chunks[i]
            for i, sim in zip(indices[0], similarities)
            if sim >= RELEVANCE_THRESHOLD
        ]

        # ----------------------------
        # PDF CONTENT FOUND
        # ----------------------------
        if relevant_chunks:
            context = "\n\n".join(relevant_chunks)

            prompt = f"""
Use ONLY the information from the PDF content below.
Paraphrasing is allowed.
Avoid repetition.

PDF CONTENT:
\"\"\"
{context}
\"\"\"

QUESTION:
{question}

ANSWER:
"""
            response = ollama.chat(
                model="deepseek-r1:1.5b",
                messages=[{"role": "user", "content": prompt}]
            )

            answer = clean_repetition(response["message"]["content"])
            return answer + "\n\nAnswer based on available PDF content."

        # ----------------------------
        # PDF EXISTS BUT ANSWER NOT FOUND
        # ----------------------------
        else:
            prompt = f"""
You are a smart study assistant.
Answer clearly and correctly.
Avoid repetition.

QUESTION:
{question}

ANSWER:
"""
            response = ollama.chat(
                model="deepseek-r1:1.5b",
                messages=[{"role": "user", "content": prompt}]
            )

            answer = clean_repetition(response["message"]["content"])
            return (
                answer
                + "\n\nAnswer not found in the provided PDF. "
                + "This answer is generated using AI knowledge."
            )

    # ============================================
    # CASE 2: NO PDF AT ALL
    # ============================================
    else:
        prompt = f"""
You are a smart study assistant.
Answer clearly and correctly.
Avoid repetition.

QUESTION:
{question}

ANSWER:
"""
        response = ollama.chat(
            model="deepseek-r1:1.5b",
            messages=[{"role": "user", "content": prompt}]
        )

        return clean_repetition(response["message"]["content"])
