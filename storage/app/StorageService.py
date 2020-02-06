import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, inspect, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import uuid

STORAGE_FOLDER_PATH = '/var/articles/'

Base = declarative_base()


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


class NewsSource(declarative_base()):
	__tablename__ = 'news_source'

	id = Column(Integer, primary_key=True)
	name = Column(String(128))
	country_code = Column(String(2))
	base_url = Column(String(256))
	created = Column(DateTime, default=datetime.datetime.now)
	last_updated = Column(DateTime, onupdate=datetime.datetime.now)


class Article(declarative_base()):
	__tablename__ = 'article'

	id = Column(Integer, primary_key=True)
	news_source_id = Column(Integer, ForeignKey(NewsSource.id))
	article_id = Column(Integer)
	is_article = Column(Boolean)
	last_updated = Column(DateTime, onupdate=datetime.datetime.now)
	title = Column(String(256))
	body_file_path = Column(String(256))
	url = Column(String(256))
	category = Column(String(64))
	article_published = Column(DateTime)
	created = Column(DateTime, default=datetime.datetime.now)
	article_last_updated = Column(DateTime)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Scrape(declarative_base()):
	__tablename__ = 'scrape'

	id = Column(Integer, primary_key=True)
	news_source_id = Column(Integer, ForeignKey(NewsSource.id))
	success = Column(Boolean)
	article_id = Column(Integer, ForeignKey(Article.id), nullable=True)
	message = Column(String(256))
	url = Column(String(256))
	created = Column(DateTime, default=datetime.datetime.now)


class StorageService:
	def __init__(self):

		# get database credentials
		database = os.getenv("PG_DATABASE")
		user = os.getenv("PG_USER")
		password = os.getenv("PG_PASSWORD")
		host = os.getenv("PG_HOST")
		port = os.getenv("PG_PORT")
		connection_string = "postgresql://" + user + ":" + password + "@" + host + ":" + port + "/" + database

		self.__engine = create_engine(connection_string, echo=False)
		Base.metadata.create_all(self.__engine)
		self.__Session = sessionmaker(bind=self.__engine)

		return

	def create_news_source(self, name, country_code, base_url):

		session = self.__Session()

		# check if exists
		if session.query(NewsSource).filter(NewsSource.name == name, NewsSource.country_code == country_code,
																							NewsSource.base_url == base_url).first():
			session.close()
			raise('Already exists')

		# add the source
		new_source = NewsSource(name=name, country_code=country_code, base_url=base_url)
		session.add(new_source)
		session.commit()

		# get the source
		source = session.query(NewsSource).filter(NewsSource.name == name, NewsSource.country_code == country_code,
																							NewsSource.base_url == base_url).first()

		source = object_as_dict(source)
		session.close()

		return source

	def get_news_source(self, news_id):
		session = self.__Session()

		source = session.query(NewsSource).filter(NewsSource.id == news_id).first()
		source = object_as_dict(source)

		session.close()

		return source

	def create_article(self, news_id, article_id, is_article, title, body, url, published, last_updated, category=None):

		session = self.__Session()

		# check if exists
		# if session.query(Article).filter(Article.name == name, NewsSource.country_code == country_code,
		# 																					NewsSource.base_url == base_url).first():
		# 	session.close()
		# 	raise('Already exists')

		# store the article body
		body_filename = str(uuid.uuid4()) + '.txt'
		print(STORAGE_FOLDER_PATH + body_filename)
		with open(STORAGE_FOLDER_PATH + body_filename, "w+") as text_file:
			text_file.write(body)

		published = datetime.datetime.strptime(published, "%Y-%m-%dT%X%z")
		last_updated = datetime.datetime.strptime(last_updated, "%Y-%m-%dT%X%z") if last_updated is not None else None
		print(news_id, article_id, is_article, title, body_filename, url, category, published, last_updated)

		# add the article to db
		article = Article(news_source_id=news_id, article_id=article_id, is_article=is_article, title=title,
											body_file_path=body_filename, url=url, category=category, article_published=published,
											article_last_updated=last_updated)
		session.add(article)
		session.commit()

		# get the source
		source = session.query(Article).filter(Article.news_source_id == news_id,
																					 Article.article_id == article_id).order_by(Article.id.desc()).first()

		session.close()

		return source.as_dict()

	def get_latest_article(self, news_id):
		session = self.__Session()

		article_nr = session.query(func.max(Article.article_id)).filter(Article.news_source_id == news_id).first()[0]

		session.close()

		response = {
			"article_nr": article_nr
		}

		return response

	# TODO
	def get_article(self, news_id, article_id):

		session = self.__Session()

		article = session.query(Article).filter(Article.news_source_id == news_id, Article.article_id == article_id).order_by(Article.id.desc()).first()

		session.close()
		# check if exists
		if not article:
			raise('Does not exist')

		response = article.as_dict()
		body_path = response['body_file_path']
		response.pop('body_file_path', None)

		with open(STORAGE_FOLDER_PATH + body_path, 'r') as file:
			body = file.read()

		response['body'] = body

		return response
