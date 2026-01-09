from fastapi import APIRouter, Depends
from ai_client import get_ai_response
from database import chat_collection
from auth import get_current_user

router = APIRouter()

@router.post("/chat")
def chat(data: dict, user=Depends(get_current_user)):

    question = data["message"]

    # 1️⃣ AI se answer lo
    answer = get_ai_response(question)

    # 2️⃣ MongoDB me save karo
    chat_collection.insert_one({
        "user": user["username"],
        "question": question,
        "answer": answer
    })

    # 3️⃣ Frontend ko reply
    return {"reply": answer}
