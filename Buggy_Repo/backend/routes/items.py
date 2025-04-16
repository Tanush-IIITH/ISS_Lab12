from fastapi import APIRouter, HTTPException
from models import Item
from bson import ObjectId

# Fix: Changed router from {} to APIRouter() to properly initialize FastAPI router
router = APIRouter()

async def get_items_collection():
    from db import init_db
    return init_db()["items_collection"]

@router.get("/")
async def get_items():
    collection = await get_items_collection()
    items = []
    async for item in collection.find():
        item["_id"] = str(item["_id"])
        items.append(item)
    return items

@router.post("/")
async def create_item(item: Item):
    collection = await get_items_collection()
    result = await collection.insert_one(item.dict())
    return {"id": str(result.inserted_id)}

# Removed: Duplicate create_item endpoint that returned {"id": "Item Inserted"}

@router.delete("/{item_id}")
async def delete_item(item_id: str):
    # Fix: Removed item_details parameter and second deletion to simplify API and avoid InvalidId errors
    # Fix: Updated response to confirm item_id deletion, avoiding misleading result2
    collection = await get_items_collection()
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count:
        return {"status": "deleted", "deleted_item_id": item_id}
    raise HTTPException(status_code=404, detail="Item not found")


# from fastapi import APIRouter, HTTPException
# from models import Item
# from bson import ObjectId

# router = APIRouter(prefix="/items", tags=["items"])

# async def get_items_collection():
#     from db import init_db
#     return init_db()["items_collection"]

# @router.get("/")
# async def get_items():
#     collection = await get_items_collection()
#     items = []
#     async for item in collection.find():
#         item["_id"] = str(item["_id"])
#         items.append(item)
#     return items

# @router.post("/")
# async def create_item(item: Item):
#     collection = await get_items_collection()
#     result = await collection.insert_one(item.dict())
#     return {"id": str(result.inserted_id)}

# @router.delete("/{item_id}")
# async def delete_item(item_id: str):
#     collection = await get_items_collection()
#     result = await collection.delete_one({"_id": ObjectId(item_id)})
#     if result.deleted_count:
#         return {"status": "deleted"}
#     raise HTTPException(status_code=404, detail="Item not found")