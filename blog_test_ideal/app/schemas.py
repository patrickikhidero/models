from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BlogPostBase(BaseModel):
    title: str
    content: str

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostUpdate(BlogPostBase):
    title: Optional[str] = None
    content: Optional[str] = None

class BlogPost(BlogPostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True