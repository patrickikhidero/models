from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    account_number: str
    balance: float

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class TransactionBase(BaseModel):
    amount: float

class TransactionCreate(TransactionBase):
    recipient_account_number: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: int
    type: str

    class Config:
        orm_mode = True