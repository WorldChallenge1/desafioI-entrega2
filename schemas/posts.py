from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str

    class Config:
        from_attributes = True
