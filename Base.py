from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI ()


class Item (BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem (BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


bag = {}


# Path parameters adding imported Path as below
@app.get ("/get-item/{item_id}")
def get_item (item_id: int = Path (None, description="The item id'like to share with you", gt=0)):
    return bag[item_id]


# Query parameters- czyli zapytania"?" http://127.0.0.1:8000/get-by-name?name=Cheese
# * adds all **kwargs
@app.get ("/get-by-name")
def get_item (name: str = Query (None, title="Name", description="Name of item", max_length=10, min_length=2)):
    for item_id in bag:
        if bag[item_id].name == name:
            return bag[item_id]
    raise HTTPException (status_code=404, detail="Item name not found")


# request body & post method
@app.post ("/create-item/{item_id}")
def create_item (item_id: int, item: Item):
    if item_id in bag:
        raise HTTPException (status_code=400, detail="Item already exists")

    bag[item_id] = item
    return bag[item_id]


# put method(update)
@app.put ("/update-item/{item_id}")
def update_item (item_id: int, item: UpdateItem):
    if item_id not in bag:
        raise HTTPException (status_code=400, detail="Item does not exist")

    if item.name != None:
        bag[item_id].name = item.name
    if item.price != None:
        bag[item_id].price = item.price
    if item.brand != None:
        bag[item_id].brand = item.brand
    return bag[item_id]


# delete method
@app.delete ("/delete-item")
def delete_item (item_id: int = Query (..., description="The Id of the item to delete", gt=0)):
    if item_id not in bag:
        raise HTTPException (status_code=400, detail="Item not found")
    del bag[item_id]
    return {"Succes": "item deleted"}
