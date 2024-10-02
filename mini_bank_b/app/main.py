from fastapi import FastAPI
from .database import engine, Base
from . import routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes.router, prefix="/bank")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mini Bank API"}