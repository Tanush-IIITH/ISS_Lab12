from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from bson import ObjectId
from datetime import datetime

# Use absolute imports instead of relative imports
from models import Item, ItemCreate, User, UserCreate
from db import init_db

app = FastAPI(title="Item Management API")

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database connection - make it compatible with synchronous client
@app.on_event("startup")
async def startup_db_client():
    app.mongodb = await init_db()
    
@app.on_event("shutdown")
def shutdown_db_client():
    if app.mongodb.get("_client"):
        app.mongodb["_client"].close()

@app.get("/")
async def root():
    return {"message": "Welcome to the Item Management API"}

# Modify route handlers to work with synchronous MongoDB operations
@app.get("/items/", response_model=List[Item])
async def read_items():
    items = list(app.mongodb["items_collection"].find())
    return items

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    new_item = item.dict()
    new_item["created_at"] = datetime.now()
    result = app.mongodb["items_collection"].insert_one(new_item)
    created_item = app.mongodb["items_collection"].find_one({"_id": result.inserted_id})
    return created_item

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="Invalid item ID format")
        
    item = app.mongodb["items_collection"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    # Check if user already exists
    existing_user = app.mongodb["users_collection"].find_one({"email": user.email})
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
    
    result = app.mongodb["users_collection"].insert_one(user_dict)
    created_user = app.mongodb["users_collection"].find_one({"_id": result.inserted_id})
    return created_user

@app.get("/users/", response_model=List[User])
async def read_users():
    users = list(app.mongodb["users_collection"].find())
    return users

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
        
    user = app.mongodb["users_collection"].find_one({"_id": ObjectId(user_id)})
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
    
    user = app.mongodb["users_collection"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    app.mongodb["users_collection"].update_one(
        {"_id": ObjectId(user_id)}, 
        {"$set": user_update}
    )
    
    updated_user = app.mongodb["users_collection"].find_one({"_id": ObjectId(user_id)})
    return updated_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)