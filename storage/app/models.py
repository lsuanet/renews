from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class NewsSource(Base):
	__tablename__ = 'news_source'

	id = Column(Integer, primary_key=True)
	name = Column(String(128))
	country_code = Column(String(2))
	base_url = Column(String(256))
	created = Column(DateTime, default=datetime.now)
	last_updated = Column(DateTime, onupdate=datetime.now)
	articles = relationship("Article")


class Article(Base):
	__tablename__ = 'article'

	id = Column(Integer, primary_key=True)
	news_source_id = Column(Integer, ForeignKey(NewsSource.id))
	article_id = Column(Integer)
	is_article = Column(Boolean)
	last_updated = Column(DateTime, onupdate=datetime.now)
	title = Column(String(256))
	body_file_path = Column(String(256))
	url = Column(String(256))
	category = Column(String(64))
	article_published = Column(DateTime)
	created = Column(DateTime, default=datetime.now)
	article_last_updated = Column(DateTime)