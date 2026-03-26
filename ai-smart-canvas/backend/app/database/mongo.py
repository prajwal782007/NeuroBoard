import motor.motor_asyncio
import os

# Connect locally or via Docker environment variables seamlessly
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.ai_smart_canvas

# Centralized collection references
boards_collection = db.get_collection("boards")
users_collection = db.get_collection("users")
sessions_collection = db.get_collection("sessions")
