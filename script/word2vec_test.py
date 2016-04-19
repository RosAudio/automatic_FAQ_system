#encoding=utf-8
# -*- coding=utf-8 -*-
from __future__ import unicode_literals
from gensim import corpora, models, similarities
import preprocessor

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MyCorpus(object):
	'''
	memory friendly corpus generator
	'''
	def __init__(self, file):
		self.__file = file

	def __iter__(self):
		for line in open(self.__file):
			yield line

def gensim_test():
	sentences = [['first','sentence'],['second','sentence']]
	model = models.Word2Vec(sentences, min_count=1)
	sim = model.similarity('first','sentence')
	most_sim = model.most_similar('first')
	print most_sim

def main(raw_corpus,raw_stoplist):
	corpus = MyCorpus(raw_corpus)
	
	# fix it
	stoplist = []
	with open(raw_stoplist,'rb') as f:
		for line in f:
			stoplist.append(line.decode) # line str
	print isinstance(stoplist[0],unicode)
	
	# stoplist = [u'@',u':',u',',u'”',u'，',u'…',u'”',u'的']

	sentences = []
	for line in corpus:
		raw_sentences = line.split('。') #split by '.'
		# print raw_sentences
		# print len(raw_sentences)
		for sentence in raw_sentences:
			if len(sentence) > 5:
				segment = preprocessor.PreProcessor(sentence)
				segment.tokenize()
				result = segment.get_result()
				ret = [word for word in result if word not in stoplist] # word unicode
				sentences.append(ret)

	for s in sentences:
		for word in s:
			print ('%s') %word
		print '-----------'
		break
	
	model = models.Word2Vec(sentences, size=200,min_count=5)
	model.save('mymodel')
	# sim = model.similarity(u'电脑',u'激光器')
	# print sim
	most_sim = model.most_similar(u'激光',topn=200)
	count = 1
	for element in most_sim:
		print ('%s  %s: %s') %(count,element[0].encode('utf-8'),element[1])	
		count += 1


if __name__ == '__main__':
	main('threebody','stoplist.txt')

	




