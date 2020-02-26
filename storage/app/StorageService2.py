from sqlalchemy.orm import Session

import models
import schemas


def create_news_source(db: Session, news_source: schemas.NewsSourceCreate):
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
	return {"news_id": news_id}


def create_article(db: Session, news_id: int, article: schemas.ArticleCreate):
	# TODO: store article in S3 compatible storage
	body_file_path = str()

	db_article = models.Article(site_article_id=article.site_article_id, title=article.title,
	                            body_file_path=body_file_path, url=article.url, category=article.category,
	                            published=article.published, article_last_updated=article.article_last_updated,
	                            news_source_id=news_id)
	db.add(db_article)
	db.commit()
	db.refresh(db_article)
	return db_article


def get_articles(db: Session, news_id: int, skip: int = 0, limit: int = 100):
	return db.query(models.Article).filter(models.Article.news_source_id == news_id).offset(skip).limit(limit).all()


def get_article(db: Session, news_id: int, article_id: int):
	return db.query(models.Article).filter(models.Article.news_source_id == news_id,
	                                       models.Article.site_article_id == article_id).first()


def delete_article(db: Session, article_id: int):
	return {"article": article_id}
