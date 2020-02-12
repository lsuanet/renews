from RequestClasses import Article, NewsSource


class StorageService:
	def __init__(self):
		return

	def create_news_source(self, news_source: NewsSource):
		return news_source

	def get_all_news_sources(self):
		return {"news_sources": "all"}

	def get_news_source(self, news_id: int):
		return {"news_id": news_id}

	def delete_news_source(self, news_id: int):
		return {"news_id": news_id}

	def create_article(self, article: Article):
		return article

	def get_all_articles(self, news_id: int):
		return {"news_id": news_id, "articles": "all"}

	def get_article(self, news_id: int, article_id: int):
		return {"news_id": news_id, "article": article_id}

	def delete_article(self, news_id: int, article_id: int):
		return {"news_id": news_id, "article": article_id}
