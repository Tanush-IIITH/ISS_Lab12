from fastapi import APIRouter, HTTPException
from models import User
from bson import ObjectId
from bson.errors import InvalidId
router = APIRouter()

async def get_users_collection():
    from db import init_db
    return init_db()["users_collection"]

#changed post to get
@router.get("/")
async def get_users():
    collection = await get_users_collection()
    users = []
    async for user in collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

# whats ur favorite genre of music ??? mine is EDM
@router.post("/")
async def create_user(user: User):
    collection = await get_users_collection()
    result = await collection.insert_one(user.dict())
    return {"id": str(result.inserted_id)}

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    try:
        obj_id=ObjectId(user_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    collection = await get_users_collection()
    #fixed: changed delete all to delete one with a filter
    result = await collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="User not found")