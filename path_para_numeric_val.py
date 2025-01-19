from fastapi import FastAPI, Query, Path

from typing import Annotated


app = FastAPI()


@app.get("/items/{item_id}")
async def get_item(item_id : Annotated[int, Path(title="ID of Item to get", ge=1)], 
                   
                   size: Annotated[float, Query(alias='size-query', gt=0, lt=10.2)],

                   q: Annotated[str | None, Query(alias="item-query")] = None,
                   ):
    results = {"item_id": item_id}

    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results
    