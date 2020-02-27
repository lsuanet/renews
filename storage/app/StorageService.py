from sqlalchemy.orm import Session
from minio import Minio
from minio.error import ResponseError
import uuid
import os

import models
import schemas


def store_string_in_minio(minio: Minio, body: str, minio_file: str):

	# create a file
	filename_server = "./tmp/%s.txt" % str(uuid.uuid4())
	with open(filename_server, "w") as f:
		f.write(body)

	# store it in minio
	try:
		minio.fput_object(bucket_name='renews', object_name=minio_file, file_path=filename_server)
	except ResponseError as err:
		print(err)

	# delete file from server
	os.remove(filename_server)
	return


def get_string_from_minio(minio: Minio, minio_file: str):

	# get file from minio
	filename_server = "./tmp/%s.txt" % str(uuid.uuid4())
	try:
		minio.fget_object('renews', minio_file, filename_server)
	except ResponseError as err:
		print(err)

	# file to string
	with open(filename_server, 'r') as file:
		data = file.read()

	# delete file from server
	os.remove(filename_server)
	return data


def create_news_source(db: Session, minio: Minio, news_source: schemas.NewsSourceCreate):
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


def delete_news_source(db: Session, minio: Minio, news_id: int):
	# TODO
	return {"news_id": news_id}


def create_article(db: Session, minio: Minio, news_id: int, article: schemas.ArticleCreate):
	minio_file = '%s/%s.txt' % (str(news_id), str(uuid.uuid4()))

	# store article body in s3
	store_string_in_minio(minio, body=article.article_body, minio_file=minio_file)

	# store article in db
	db_article = models.Article(site_article_id=article.site_article_id, title=article.title,
	                            body_file_path=minio_file, url=article.url, category=article.category,
	                            published=article.published, article_last_updated=article.article_last_updated,
	                            news_source_id=news_id)
	db.add(db_article)
	db.commit()
	db.refresh(db_article)

	db_article.article_body = get_string_from_minio(minio, minio_file=db_article.body_file_path)

	return db_article


def get_articles(db: Session, minio: Minio, news_id: int, skip: int = 0, limit: int = 100):
	# TODO: get articles from s3
	return db.query(models.Article).filter(models.Article.news_source_id == news_id).offset(skip).limit(limit).all()


def get_article(db: Session, minio: Minio, news_id: int, article_id: int):
	article = db.query(models.Article).filter(models.Article.news_source_id == news_id,
	                                       models.Article.site_article_id == article_id).first()

	article.article_body = get_string_from_minio(minio, minio_file=article.body_file_path)

	return article


def delete_article(db: Session, minio: Minio, article_id: int):
	return {"article": article_id}
