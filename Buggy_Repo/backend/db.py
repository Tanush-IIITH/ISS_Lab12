from pymongo import MongoClient
import os
from typing import Dict, Any
import asyncio

async def init_db() -> Dict[str, Any]:
    """Initialize database connection and return collections.
    
    Returns:
        Dict[str, Any]: A dictionary of MongoDB collections
        
    Raises:
        Exception: If connection to MongoDB fails
    """
    client = None
    try:
        MONGO_URI = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        # Use standard pymongo client instead of motor
        client = MongoClient(MONGO_URI, connect=False)
        db = client["testdb"]
        
        # Verify connection by pinging the server (non-async way)
        client.admin.command('ping')
        print("Connected successfully to MongoDB")
        
        # Return collections dictionary
        return {
            "item_collection": db["item"],
            "users_collection": db["users"],
            "_client": client  # Include client for proper cleanup
        }
        
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        if client:
            client.close()
        raise
