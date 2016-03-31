# encoding=utf-8

class Matcher(object):
	def __init__(self,question,update = False):
		'''
		'''
		self.__question = question
		self.__pos # ???
		self.__words = {'word1':[],'word2':[]}

	def candidate_select(self):
		'''

		'''
		for w in self.__question:
			if w in self.__words:
				

