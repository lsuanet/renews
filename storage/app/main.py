from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

import schemas, models
import StorageService2 as storage
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# start the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s,%(message)s', datefmt='%Y-%m-%d %X')
logger = logging.getLogger('storage')

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post('/news-sources', response_model=schemas.NewsSource)
def create_news_source(news_source: schemas.NewsSourceCreate, db: Session = Depends(get_db)):
    # TODO check if already exists
    return storage.create_news_source(db, news_source)


@app.get('/news-sources', response_model=List[schemas.NewsSource])
def get_news_sources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return storage.get_news_sources(db, skip=skip, limit=limit)


@app.get('/news-sources/{news_id}', response_model=schemas.NewsSource)
def get_news_source(news_id: int, db: Session = Depends(get_db)):
    news_source = storage.get_news_source(db, news_id=news_id)
    if news_source is None:
        raise HTTPException(status_code=404, detail="News source not found")
    return news_source


@app.delete('/news-sources/{news_id}')
def delete_news_source(news_id: int):
    # TODO
    return # storage.delete_news_source(news_id)


@app.post('/news-sources/{news_id}/articles', response_model=schemas.Article)
def create_article(news_id: int, article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    # TODO check if exists
    return storage.create_article(db, news_id=news_id, article=article)


@app.get('/news-sources/{news_id}/articles', response_model=List[schemas.Article])
def get_articles(news_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return storage.get_articles(db, news_id=news_id, skip=skip, limit=limit)


@app.get('/news-sources/{news_id}/articles/{article_id}', response_model=schemas.Article)
def get_article(news_id: int, article_id: int, db: Session = Depends(get_db)):
    article = storage.get_article(db, news_id=news_id, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.delete('/news-sources/{news_id}/articles/{article_id}')
def delete_article(news_id: int, article_id: int):
    # TODO
    return # storage.delete_article(news_id, article_id)
