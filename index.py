from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Item data model
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# In-memory "database"
items_db = {}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI CRUD example!"}

# Get all items
@app.get("/items", response_model=List[Item])
def get_items():
    return list(items_db.values())

# Get item by id
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

# Create new item
@app.post("/items", response_model=Item)
def create_item(item: Item):
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item ID already exists")
    items_db[item.id] = item
    return item

# Update item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return item

# Delete item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"detail": f"Item {item_id} deleted"}



