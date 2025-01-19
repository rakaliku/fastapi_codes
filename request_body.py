from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    print(type(item_dict))
    print(f"Item dict is {item_dict}")
    if item_dict['tax']:
        price_with_tax = item_dict["price"] + item_dict["tax"]
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     item_dict = item.dict()
#     if item_id:
#         item_dict.update({"item_id": item_id})
#     return item_dict

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, qeury_parameter: str | None = None ):
    result = {"item_id": item_id, **item.dict()}
    
    if qeury_parameter:
        result.update({"qeury_parameter": qeury_parameter})
    return result