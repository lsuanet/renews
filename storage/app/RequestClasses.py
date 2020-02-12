from pydantic import BaseModel
from datetime import datetime


class Article(BaseModel):
    news_id: int
    article_id: int
    is_article: bool
    url: str
    title: str = None
    article_body: str = None
    published: datetime = None
    last_updated: datetime = None
    category: str = None


class NewsSource(BaseModel):
    name: str
    country_code: str
    base_ur: str
