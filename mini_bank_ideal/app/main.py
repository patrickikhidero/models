# app/main.py
from fastapi import FastAPI
from .api import router

app = FastAPI()

app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mini Bank API"}
