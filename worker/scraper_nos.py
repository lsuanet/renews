import urllib.request
from worker.scraper_components.nos import url_generator, get_contents

ARTICLE_ID = 2317223

for url in url_generator(ARTICLE_ID):

	try:
		request = urllib.request.urlopen(url)

	except:
		print('Not found: ' + url)
		continue

	content = request.read()
	try:
		title, published, modified, body_list = get_contents(content, url)
		print('Found: ' + url)

		# write to database
		print(title)
		print(published)
		print(modified)
		print(body_list)
	except:
		print('Found, but failed to scrape: ' + url)

	break
