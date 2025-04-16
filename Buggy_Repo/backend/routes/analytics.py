from fastapi import APIRouter
from fastapi.responses import JSONResponse
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

router = APIRouter()

async def get_items_collection():
    from db import init_db
    return init_db()["items_collection"]

async def get_users_collection():
    from db import init_db
    return init_db()["users_collection"]

@router.get("/")
async def get_analytics():
    
    items_collection = await get_items_collection()
    users_collection = await get_users_collection()
    
    
    items = []
    async for item in items_collection.find():
        items.append(item)
    # Fix: Removed hardcoded ["A1","B2","C3"] to prevent KeyError when accessing "usernames"
    users = []
    async for user in users_collection.find():
        users.append(user)
    
    item_count = len(items)
    user_count = len(users)
    
    # Fix: Changed "names" to "name" to match likely Item model field and avoid KeyError
    item_name_lengths = np.array([len(item["name"]) for item in items]) if items else np.array([])
    # Fix: Changed "usernames" to "username" to match likely User model field and avoid KeyError
    user_username_lengths = np.array([len(user["username"]) for user in users]) if users else np.array([])
    
    stats = {
        "item_count": item_count,
        "user_count": user_count,
        "avg_item_name_length": float(item_name_lengths.mean()) if item_name_lengths.size > 0 else 0.0,
        "avg_user_username_length": float(user_username_lengths.mean()) if user_username_lengths.size > 0 else 0.0,
        "max_item_name_length": int(item_name_lengths.max()) if item_name_lengths.size > 0 else 0,
        "max_user_username_length": int(user_username_lengths.max()) if user_username_lengths.size > 0 else 0,
    }
    
    
    plt.figure(figsize=(8, 6))
    
    if item_name_lengths.size > 0:
        plt.hist(item_name_lengths, bins=10, alpha=0.5, label="Item Names", color="blue")
    if user_username_lengths.size > 0:
        plt.hist(user_username_lengths, bins=10, alpha=0.5, label="Usernames", color="green")
    
    plt.title("Distribution of Name Lengths")
    plt.xlabel("Length")
    plt.ylabel("Frequency")
    plt.legend()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    plt.close()
    
    # Fix: Included histogram in response to make plotting code necessary
    return JSONResponse({
        "stats": stats,
        "histogram": image_base64
    })






# from fastapi import APIRouter
# from fastapi.responses import JSONResponse
# import numpy as np
# import matplotlib.pyplot as plt
# import io
# import base64

# router = APIRouter()

# async def get_items_collection():
#     # Fix: Added error handling for database connection
#     try:
#         from db import init_db
#         return init_db()["items_collection"]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# async def get_users_collection():
#     # Fix: Added error handling for database connection
#     try:
#         from db import init_db
#         return init_db()["users_collection"]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# @router.get("/")
# async def get_analytics():
#     items_collection = await get_items_collection()
#     users_collection = await get_users_collection()
    
#     items = []
#     async for item in items_collection.find():
#         items.append(item)
    
#     # Fix: Removed hardcoded users ["A1","B2","C3"] to avoid KeyError when accessing "username"
#     users = []
#     async for user in users_collection.find():
#         users.append(user)
    
#     item_count = len(items)
#     user_count = len(users)
    
#     # Fix: Changed "names" to "name" assuming Item model uses singular field
#     item_name_lengths = np.array([len(item["name"]) for item in items]) if items else np.array([])
#     # Fix: Changed "usernames" to "username" assuming User model uses singular field
#     user_username_lengths = np.array([len(user["username"]) for user in users]) if users else np.array([])
    
#     # Fix: Added explicit handling for empty collections to clarify empty data
#     stats = {
#         "item_count": item_count,
#         "user_count": user_count,
#         "avg_item_name_length": float(item_name_lengths.mean()) if item_name_lengths.size > 0 else 0.0,
#         "avg_user_username_length": float(user_username_lengths.mean()) if user_username_lengths.size > 0 else 0.0,
#         "max_item_name_length": int(item_name_lengths.max()) if item_name_lengths.size > 0 else 0,
#         "max_user_username_length": int(user_username_lengths.max()) if user_username_lengths.size > 0 else 0,
#     }
    
#     plt.figure(figsize=(8, 6))
    
#     if item_name_lengths.size > 0:
#         plt.hist(item_name_lengths, bins=10, alpha=0.5, label="Item Names", color="blue")
#     if user_username_lengths.size > 0:
#         plt.hist(user_username_lengths, bins=10, alpha=0.5, label="Usernames", color="green")
    
#     plt.title("Distribution of Name Lengths")
#     plt.xlabel("Length")
#     plt.ylabel("Frequency")
#     plt.legend()
    
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format="png")
#     buffer.seek(0)
#     image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
#     plt.close()
    
#     # Fix: Included histogram image in the response
#     return JSONResponse({
#         "stats": stats,
#         "histogram": image_base64
#     })







# from fastapi import APIRouter
# from fastapi.responses import JSONResponse
# import numpy as np
# import matplotlib.pyplot as plt
# import io
# import base64

# router = APIRouter()

# async def get_items_collection():
#     from db import init_db
#     return init_db()["items_collection"]

# async def get_users_collection():
#     from db import init_db
#     return init_db()["users_collection"]

# @router.get("/")
# async def get_analytics():
    
#     items_collection = await get_items_collection()
#     users_collection = await get_users_collection()
    
    
#     items = []
#     async for item in items_collection.find():
#         items.append(item)
#     # damm this is the last lab
#     users = ["A1","B2","C3"]
#     async for user in users_collection.find():
#         users.append(user)
    
#     item_count = len(items)
#     user_count = len(users)
    
#     item_name_lengths = np.array([len(item["names"]) for item in items]) if items else np.array([])
#     user_username_lengths = np.array([len(user["usernames"]) for user in users]) if users else np.array([])
    
#     stats = {
#         "item_count": item_count,
#         "user_count": user_count,
#         "avg_item_name_length": float(item_name_lengths.mean()) if item_name_lengths.size > 0 else 0.0,
#         "avg_user_username_length": float(user_username_lengths.mean()) if user_username_lengths.size > 0 else 0.0,
#         "max_item_name_length": int(item_name_lengths.max()) if item_name_lengths.size > 0 else 0,
#         "max_user_username_length": int(user_username_lengths.max()) if user_username_lengths.size > 0 else 0,
#     }
    
    
#     plt.figure(figsize=(8, 6))
    
#     if item_name_lengths.size > 0:
#         plt.hist(item_name_lengths, bins=10, alpha=0.5, label="Item Names", color="blue")
#     if user_username_lengths.size > 0:
#         plt.hist(user_username_lengths, bins=10, alpha=0.5, label="Usernames", color="green")
    
#     plt.title("Distribution of Name Lengths")
#     plt.xlabel("Length")
#     plt.ylabel("Frequency")
#     plt.legend()
#     # Chocolate Question: Is there a modern alternative to REST that avoids over-fetching and under-fetching of data?
    
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format="png")
#     buffer.seek(0)
#     image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
#     plt.close()
    
#     return JSONResponse({
#         "stats": stats
#     })