import requests
from worker.scraper_components.nos import url_generator, get_contents

ARTICLE_ID = 2319748
NEWS_SOURCE_ID = 1
STORAGE_URL = 'http://localhost:5000'

title = None

url = 'https://nos.nl/artikel/' + str(ARTICLE_ID)

r = requests.get(url)

content = r.text

try:
	title, published, modified, body = get_contents(content)
	print('Found: ' + url)

	data = {
		"title": title,
		"news_id": 1,
		"article_id": ARTICLE_ID,
		"is_article": True,
		"url": url,
		"body": body,
		"published": published,
		"last_updated": modified,
		"category": "Unknown"
	}

	# write to database

	requests.post(STORAGE_URL + '/articles', json=data)

except:
	print('Found, but failed to scrape: ' + url)
	# error
