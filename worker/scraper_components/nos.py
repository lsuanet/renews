import re
from bs4 import BeautifulSoup

BASE_URL = ['https://nos.nl/', 'https://jeugdjournaal.nl/']
URL_TYPES = ['video/', 'artikel/', 'nieuwsuur/artikel/', 'liveblog/']


def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext


def get_contents(html, url):

	if url.startswith(BASE_URL[1]) or \
					(url.startswith(BASE_URL[0] + URL_TYPES[0]) or url.startswith(BASE_URL[0] + URL_TYPES[3])):
		return None, None, None, None

	soup = BeautifulSoup(html)

	title = soup.find('h1').string.strip()
	body_list = soup.find('div', attrs={"class": re.compile("contentBlock")}).find_all('p', attrs={
		"class": re.compile("text")})
	body_list = [cleanhtml(str(item)) for item in body_list]
	body = body_list[0]
	if len(body_list) > 1:
		for paragraph in body_list[1:]:
			body += "\n" + paragraph

	published = soup.find('span', attrs={"class": re.compile("published")}).time['datetime']
	modified = None
	if soup.find('span', attrs={"class": re.compile("modified")}):
		modified = soup.find('span', attrs={"class": re.compile("modified")}).time['datetime']

	return title, published, modified, body


def url_generator(article_id):
	for base in BASE_URL:
		for item in URL_TYPES:
			url = base + item + str(article_id)
			yield url, base == BASE_URL[0] and item == URL_TYPES[1]
