from pydantic import BaseModel

# Fix: Changed Item to inherit from BaseModel to enable Pydantic validation
class Item(BaseModel):
    # Fix: Changed name type from int to str to match usage in analytics.py
    name: str
    description: str

class User(BaseModel):
    username: str
    bio: str