from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import asyncio
from bson import ObjectId
from datetime import datetime

from .models import Item, ItemCreate, User, UserCreate
from .db import init_db

app = FastAPI(title="Item Management API")

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize database connection
db = init_db()
items_collection = db["items_collection"]
users_collection = db["users_collection"]

@app.get("/")
async def root():
    return {"message": "Welcome to the Item Management API"}

@app.get("/items/", response_model=List[Item])
async def read_items():
    items = await items_collection.find().to_list(1000)
    return items

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    new_item = item.dict()
    new_item["created_at"] = datetime.now()
    result = await items_collection.insert_one(new_item)
    created_item = await items_collection.find_one({"_id": result.inserted_id})
    return created_item

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="Invalid item ID format")
        
    item = await items_collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    user_dict = user.dict()
    # Don't store plain text password in a real app
    # Here you would hash the password
    
    # Add created_at timestamp
    user_dict["created_at"] = datetime.now()
    
    result = await users_collection.insert_one(user_dict)
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    return created_user

@app.get("/users/", response_model=List[User])
async def read_users():
    users = await users_collection.find().to_list(1000)
    return users

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
        
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: dict):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    # Don't allow password updates through this endpoint
    if "password" in user_update:
        del user_update["password"]
    
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    await users_collection.update_one(
        {"_id": ObjectId(user_id)}, 
        {"$set": user_update}
    )
    
    updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    return updated_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)