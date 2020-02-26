from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class NewsSource(Base):
	__tablename__ = 'news_source'

	id = Column(Integer, primary_key=True)
	name = Column(String(128))
	country_code = Column(String(2))
	base_url = Column(String(256))
	created = Column(DateTime, default=datetime.now)
	last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
	articles = relationship("Article", back_populates="news_source")


class Article(Base):
	__tablename__ = 'article'

	id = Column(Integer, primary_key=True)
	site_article_id = Column(Integer)
	last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
	title = Column(String(256))
	body_file_path = Column(String(256))
	url = Column(String(256))
	category = Column(String(64))
	published = Column(DateTime)
	created = Column(DateTime, default=datetime.now)
	article_last_updated = Column(DateTime)
	news_source_id = Column(Integer, ForeignKey(NewsSource.id))
	news_source = relationship("NewsSource", back_populates="articles")
