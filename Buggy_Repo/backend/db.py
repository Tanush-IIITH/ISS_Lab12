from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import Dict, Any

def init_db() -> Dict[str, Any]:
    """Initialize database connection and return collections."""
    try:
        MONGO_URI = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        client = AsyncIOMotorClient(MONGO_URI)
        db = client["testdb"]
        
        # Make sure the collections exist
        collections = {
            "items_collection": db["items"],  # Fixed the collection name to "items"
            "users_collection": db["users"]
        }
        
        # Ping the server to verify connection
        client.admin.command('ping')
        print("Connected successfully to MongoDB")
        return collections
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise