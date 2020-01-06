import urllib.request
from worker.scraper_components.nos import url_generator, get_contents

ARTICLE_ID = 2317222
NEWS_SOURCE_ID = 1
STORAGE_URL = ''

title = None

for url, is_correct_page in url_generator(ARTICLE_ID):

	try:
		request = urllib.request.urlopen(url)

	except:
		print('Not found: ' + url)
		continue

	content = request.read()
	if is_correct_page:
		try:
			title, published, modified, body = get_contents(content, url)
			print('Found: ' + url)

			# write to database
			print(title)
			print(published)
			print(modified)
			print(body)
		except:
			print('Found, but failed to scrape: ' + url)
			# error

	else:
		print('Found, but not correct page: ' + url)

		# write to db

	break
