from fastapi import FastAPI
import logging

from RequestClasses import Article, NewsSource
from StorageService2 import StorageService


# start the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s,%(message)s', datefmt='%Y-%m-%d %X')
logger = logging.getLogger('storage')

storage = StorageService()
app = FastAPI()


@app.post('/news-sources')
def create_news_source(news_source: NewsSource):
    # TODO
    return storage.create_news_source(news_source)


@app.get('/news-sources')
def get_all_news_sources():
    # TODO
    return storage.get_all_news_sources()


@app.get('/news-sources/{news_id}')
def get_news_source(news_id: int):
    # TODO
    return storage.get_news_source(news_id)


@app.delete('/news-sources/{news_id}')
def delete_news_source(news_id: int):
    # TODO
    return storage.delete_news_source(news_id)


@app.post('/news-sources/{news_id}/articles')
def create_article(article: Article):
    # TODO
    return storage.create_article(article)


@app.get('/news-sources/{news_id}/articles')
def get_all_articles(news_id: int):
    # TODO
    return storage.get_all_articles(news_id)


@app.get('/news-sources/{news_id}/articles/{article_id}')
def get_article(news_id: int, article_id: int):
    # TODO
    return storage.get_article(news_id, article_id)


@app.delete('/news-sources/{news_id}/articles/{article_id}')
def delete_article(news_id: int, article_id: int):
    # TODO
    return storage.delete_article(news_id, article_id)
