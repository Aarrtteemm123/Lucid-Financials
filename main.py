from fastapi import FastAPI
from starlette.requests import Request
from routes import view_router

app = FastAPI()

app.include_router(view_router, prefix="/api")

@app.get("/healthcheck")
async def healthcheck(request: Request):
    return {"status": "app server is running..."}
