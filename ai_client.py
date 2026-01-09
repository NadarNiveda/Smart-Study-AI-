import requests

SMARTSTUDY_AI_URL = "http://127.0.0.1:8001/ask"

def get_ai_response(question: str):
    response = requests.post(
        SMARTSTUDY_AI_URL,
        json={"question": question},
        timeout=60
    )
    return response.json()["answer"]
