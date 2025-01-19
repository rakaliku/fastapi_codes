from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def custom_middleware_func(request: Request, call_next):
    # Your custom middleware code here
    print("Middleware executed")
    response = await call_next(request)
    return response

@app.get("/middle/")
async def home():
    print("hi.....")
    return {"midle ware code": "worked"}