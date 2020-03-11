import requests
from worker.scraper_components.nos import get_contents

NOS_URL = 'https://nos.nl'
STORAGE_URL = 'http://localhost:5000'
ARTICLE = '2321869'

url = NOS_URL + '/artikel/' + ARTICLE
content = requests.get(url).text
title, published, modified, body = get_contents(content)

data = {
	"title": title,
	"news_id": 1,
	"article_id": ARTICLE,
	"is_article": True,
	"url": url,
	"body": body,
	"published": published,
	"last_updated": modified,
	"category": "Unknown"
}
print(data)
print("Store article " + str(ARTICLE))
r = requests.post(STORAGE_URL + '/articles', json=data)
print(r.status_code)
print(r.content)

