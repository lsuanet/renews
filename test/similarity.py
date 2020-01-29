import numpy as np
import math
from bert_serving.client import BertClient
import datetime


def dutch_text_similarity(one, two):
	'''
	Get the similarity of two BERTje vectorized strings
	:param one: BERTje vector
	:param two: BERTje vector
	:return:
	'''

	cosine = np.dot(one, two) / (np.linalg.norm(one) * np.linalg.norm(two))
	return 1 / (1 + math.exp(-100 * (cosine - 0.95)))


def dutch_paragraph_similarity(one, two):
	'''
	Find the paragraphs that are most different from the other article
	:param one: list of strings (paragraphs of article 1)
	:param two: list of strings (paragraphs of article 2)
	:return:
	'''
	# encode the paragraphs
	bc = BertClient()
	vec1 = bc.encode(one)
	vec2 = bc.encode(two)

	# for every paragraph in both articles, find the maximum similarity to every other paragraph in the other article
	max_one = [0] * len(vec1)
	max_two = [0] * len(vec2)
	for i, p in enumerate(vec1):
		for j, q in enumerate(vec2):
			sim = dutch_text_similarity(p, q)
			if sim > max_one[i]:
				max_one[i] = sim
			if sim > max_two[j]:
				max_two[j] = sim

	# find the paragraph that is least similar to all paragraphs in the other article
	print(max_one)
	print(max_one.index(min(max_one)))
	print(max_two)
	print(max_two.index(min(max_two)))

	return


def dutch_article_similarity(one, two):
	'''
	Calculate how similar two articles are
	:param one: string (article 1)
	:param two: string (article 2)
	:return: float similarity
	'''
	# encode the paragraphs
	bc = BertClient()
	vec1, vec2 = bc.encode([one, two])

	return dutch_text_similarity(vec1, vec2)


a = './articles/1-nos.txt'
b = './articles/2-nu.txt'

with open(a, 'r') as file:
	article1 = file.read().replace('\n', '')
with open(a, 'r') as file:
	paragraphs1 = [x.replace('\n', '') for x in file]
with open(b, 'r') as file:
	article2 = file.read().replace('\n', '')
with open(b, 'r') as file:
	paragraphs2 = [x.replace('\n', '') for x in file]

print(dutch_article_similarity(article1, article2))
dutch_paragraph_similarity(paragraphs1, paragraphs2)

