from pydantic import BaseModel
from typing import Optional
from datetime import datetime




class ArticleBase(BaseModel):
    title: str
    url: str
    source: str


class ArticleCreate(ArticleBase):
    summary: Optional[str] = None
    date: Optional[str] = None


class Article(ArticleBase):
    id: int
    summary: Optional[str]
    date: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True