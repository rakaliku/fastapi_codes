from fastapi import FastAPI, Header

from typing import Annotated 


app = FastAPI()


@app.get("/items/")
async def read_item(user_Agent: Annotated[str|None, Header()]):
    return {"User-Agent": user_Agent}
