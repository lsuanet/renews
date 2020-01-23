import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from worker.scraper_components.nos import get_contents

NOS_URL = 'https://nos.nl'
STORAGE_URL = 'http://localhost:5000'
LATEST_URL = 'http://localhost:5000/articles/getLatest'

r = requests.get(NOS_URL)
soup = BeautifulSoup(r.text, features="html.parser")
a = soup.find_all('a', attrs={"href": re.compile("^/artikel/*")})
article_nrs = list(set([int(i['href'].split('/')[2].split('-')[0]) for i in a]))

# get latest article nr
params = {"news_id": 1}
r = requests.get(LATEST_URL, params=params)
article_nr = r.json()['article_nr']

# get list of unscraped article numbers
unscraped = [i for i in article_nrs if i > article_nr]

# scrape unscraped
for article in unscraped:
	url = NOS_URL + '/artikel/' + str(article)
	content = requests.get(url).text
	title, published, modified, body = get_contents(content)

	data = {
		"title": title,
		"news_id": 1,
		"article_id": article,
		"is_article": True,
		"url": url,
		"body": body,
		"published": published,
		"last_updated": modified,
		"category": "Unknown"
	}
	print("Store article " + str(article))
	requests.post(STORAGE_URL + '/articles', json=data)
	sleep(5)
