from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import Dict, Any

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
        client = AsyncIOMotorClient(MONGO_URI)
        db = client["testdb"]
        
        # Verify connection by pinging the server
        await client.admin.command('ping')
        print("Connected successfully to MongoDB")
        
        # Return collections dictionary
        return {
            "items_collection": db["items"],
            "users_collection": db["users"],
            "_client": client  # Include client for proper cleanup
        }
        
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        if client:
            client.close()
        raise
