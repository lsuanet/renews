from flask import Flask, request
import logging
import json
from flasgger import Swagger, swag_from
from StorageService import StorageService

# start the logger
logging.basicConfig(filename='/logs/app.log', level=logging.INFO,
										format='%(asctime)s,%(message)s', datefmt='%Y-%m-%d %X')
logger = logging.getLogger('storage')

# OpenAPI spec
template = {
	"swagger": "2.0",
	"uiversion": 3,
	"info": {
		"title": "Storage API for reNews",
		"description": "API for managing the renews database.",
		# "contact": {
		# 	"responsibleOrganization": "ME",
		# 	"responsibleDeveloper": "Me",
		# 	"email": "me@me.com",
		# 	"url": "www.me.com",
		# },
		# "termsOfService": "http://me.com/terms",
		"version": "0.0.1"
	},
	# "host": "mysite.com",  # overrides localhost:500
	# "basePath": "/api",  # base bash for blueprint registration
	# "schemes": [
	# 	"http",
	# 	"https"
	# ],
	# "operationId": "getmyData"
}

storage = StorageService()

app = Flask(__name__)
swagger = Swagger(app, template=template)


@app.route('/news-source/', methods=['POST'])
@swag_from('../docs/create_news_source.yml')
def create_news_source():
	'''
	Create a news source
	:return:
	'''
	response = dict()

	try:
		# get arguments from body
		body = request.json
		logger.info('Request body:\n' + json.dumps(body))

		name = body['name']
		country_code = body['country_code']
		base_url = body['base_url']

		response = storage.create_news_source(name=name, country_code=country_code, base_url=base_url)

		status_code = 202
		logger.info('Success.')

	except Exception as e:
		logger.error('Error: ' + str(e))
		response['message'] = "Oops, something went wrong"
		response['error'] = str(e)
		status_code = 400

	return response, status_code


@app.route('/news-source/<name>', methods=['GET'])
@swag_from('../docs/get_news_source.yml')
def get_news_source(name):
	'''
	Create a news source
	:return:
	'''
	response = dict()

	try:
		# get arguments from body
		# body = request.json
		# logger.info('Request body:\n' + json.dumps(body))

		response = storage.get_news_source(name=name)

		status_code = 202
		logger.info('Success.')

	except Exception as e:
		logger.error('Error: ' + str(e))
		response['message'] = "Oops, something went wrong"
		response['error'] = str(e)
		status_code = 400

	return response, status_code

@app.route('/news-source/<news_id>/', methods=['POST'])
@swag_from('../docs/create_article.yml')
def create_article(news_id):
	'''
	Create an article
	:return:
	'''
	response = dict()

	try:
		# get arguments from body
		# body = request.json
		# logger.info('Request body:\n' + json.dumps(body))

		response = storage.create_article(news_id=news_id)

		status_code = 202
		logger.info('Success.')

	except Exception as e:
		logger.error('Error: ' + str(e))
		response['message'] = "Oops, something went wrong"
		response['error'] = str(e)
		status_code = 400

	return response, status_code
