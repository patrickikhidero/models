# app/schemas.py
from pydantic import BaseModel

class UserDetailsResponse(BaseModel):
    username: str
    account_number: str
    balance: float

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    balance: float

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
