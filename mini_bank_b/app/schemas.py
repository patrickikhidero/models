from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TransactionBase(BaseModel):
    amount: float
    recipient_account: str = None

class TransactionCreate(TransactionBase):
    pass

class UserBalance(BaseModel):
    balance: float