from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

from database import users_collection, chat_collection
from ai_client import get_ai_response   # 🔴 SmartStudy AI import

app = FastAPI()

# -------- CORS (React ke liye) --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # production me specific origin dena
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------- MODELS --------
class Signup(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class ChatRequest(BaseModel):
    message: str
    username: str | None = None

class ChatResponse(BaseModel):
    reply: str


# -------- UTILS --------
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


# -------- ROUTES --------
@app.get("/")
def root():
    return {"message": "Smart-Study Backend Running"}


@app.post("/signup")
def signup(data: Signup):
    if users_collection.find_one({"username": data.username}):
        raise HTTPException(status_code=400, detail="User already exists")

    users_collection.insert_one({
        "username": data.username,
        "password": hash_password(data.password)
    })

    return {"message": "Signup successful"}


@app.post("/login")
def login(data: Login):
    user = users_collection.find_one({"username": data.username})

    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}


@app.post("/chat", response_model=ChatResponse)
def chat(data: ChatRequest):
    """
    1. User message React se aata hai
    2. SmartStudy AI ko bheja jata hai
    3. AI ka answer milta hai
    4. MongoDB me save hota hai
    5. Frontend ko reply jata hai
    """

    # 🔹 SmartStudy AI se real answer
    reply = get_ai_response(data.message)

    # 🔹 MongoDB me chat save
    chat_collection.insert_one({
        "username": data.username,
        "message": data.message,
        "reply": reply
    })

    return {"reply": reply}
