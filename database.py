from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["ChatbotDB"]

user_collection = db["users"]
chat_collection = db["chats"]
