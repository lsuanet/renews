from pydantic import BaseModel
from datetime import datetime
from typing import List


class ArticleBase(BaseModel):
    site_article_id: int
    url: str
    news_source_id: int
    title: str = None
    article_body: str = None
    published: datetime = None
    article_last_updated: datetime = None
    category: str = None


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    created: datetime
    last_updated: datetime

    class Config:
        orm_mode = True


class NewsSourceBase(BaseModel):
    name: str
    country_code: str
    base_url: str


class NewsSourceCreate(NewsSourceBase):
    pass


class NewsSource(NewsSourceBase):
    id: int
    created: datetime
    last_updated: datetime

    class Config:
        orm_mode = True
