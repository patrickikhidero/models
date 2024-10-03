from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    time_created: datetime
    time_updated: datetime

    class Config:
        orm_mode = True