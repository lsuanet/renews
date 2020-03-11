from sqlalchemy.orm import Session
from minio import Minio
import uuid

import minio_service as minio_service

import models
import schemas


def create_news_source(db: Session, news_source: schemas.NewsSourceCreate):
    # TODO check if already exists
    db_news_source = models.NewsSource(name=news_source.name, country_code=news_source.country_code,
                                       base_url=news_source.base_url)
    db.add(db_news_source)
    db.commit()
    db.refresh(db_news_source)

    return db_news_source


def get_news_sources(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.NewsSource).offset(skip).limit(limit).all()


def get_news_source(db: Session, news_id: int):
    return db.query(models.NewsSource).filter(models.NewsSource.id == news_id).first()


def delete_news_source(db: Session, news_id: int):
    # TODO: handle orphan articles
    db.query(models.NewsSource).filter(models.NewsSource.id == news_id).delete()
    db.commit()
    return {"news_id": news_id}


def create_article(db: Session, minio: Minio, article: schemas.ArticleCreate):
    minio_file = '%s/%s.txt' % (str(article.news_source_id), str(uuid.uuid4()))

    # store article body in s3
    minio_service.store_string(minio, body=article.article_body, minio_file=minio_file)

    # store article in db
    db_article = models.Article(site_article_id=article.site_article_id, title=article.title,
                                body_file_path=minio_file, url=article.url, category=article.category,
                                published=article.published, article_last_updated=article.article_last_updated,
                                news_source_id=article.news_source_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    db_article.article_body = minio_service.get_string(minio, minio_file=db_article.body_file_path)

    return db_article


def get_articles(db: Session, minio: Minio, news_id: int, skip: int = 0, limit: int = 100):
    articles = db.query(models.Article).filter(models.Article.news_source_id == news_id).offset(skip).limit(limit).all()
    articles_w_body = list()
    for article in articles:
        article.article_body = minio_service.get_string(minio, minio_file=article.body_file_path)
        articles_w_body.append(article)

    return articles_w_body


def get_article(db: Session, minio: Minio, article_id: int):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if article is None:
        return article

    article.article_body = minio_service.get_string(minio, minio_file=article.body_file_path)

    return article


def delete_article(db: Session, minio: Minio, article_id: int):
    # delete from minio
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    path = article.body_file_path
    minio_service.delete_object(minio, minio_file=path)

    # delete from db
    db.query(models.Article).filter(models.Article.id == article_id).delete()
    db.commit()
    return
