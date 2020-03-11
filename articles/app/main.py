from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging
from minio import Minio

import schemas
import models
import storage as storage
from database import engine
from dependencies import get_db, get_minio

models.Base.metadata.create_all(bind=engine)

# start the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s,%(message)s', datefmt='%Y-%m-%d %X')
logger = logging.getLogger('storage')

app = FastAPI()


@app.post('/news-sources', response_model=schemas.NewsSource)
def create_news_source(news_source: schemas.NewsSourceCreate, db: Session = Depends(get_db)):
    return storage.create_news_source(db, news_source=news_source)


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
    return  # storage.delete_news_source(news_id)


@app.post('/articles', response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db),
                   minio: Minio = Depends(get_minio)):
    # TODO check if exists
    return storage.create_article(db, minio=minio, article=article)


@app.get('/articles', response_model=List[schemas.Article])
def get_articles(news_source_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                 minio: Minio = Depends(get_minio)):
    return storage.get_articles(db, minio=minio, news_id=news_source_id, skip=skip, limit=limit)


@app.get('/articles/{article_id}', response_model=schemas.Article)
def get_article(article_id: int, db: Session = Depends(get_db),
                minio: Minio = Depends(get_minio)):
    article = storage.get_article(db, minio=minio, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.delete('/articles/{article_id}')
def delete_article(article_id: int, db: Session = Depends(get_db), minio: Minio = Depends(get_minio)):
    return storage.delete_article(db=db, minio=minio, article_id=article_id)
