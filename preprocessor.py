# encoding=utf-8

try:
	import jieba # jieba tokenizer
except e:
	print ('an error occured when importing "jieba"')


class PreProcessor(object):
	'''
	preprocssor to tokenize the text, replace the synonym and pronoun 
	'''
	def __init__(self, text, *args, **kw):
		'''
		param@text: text to tokenize
		param@args: pre-texts
		'''
		self.__text = text
		self.__tokenized_ret = []
		self.__result = []
		if len(args) != 0:
			self.__pre_text = args
		else:
			self.__pre_text = []

	def tokenize(self, tokenizer = 'jieba', cut_all = False):
		'''
		param@tokenizer: jieba or NLPIR
		param@cut_all: True - cut all mode / False - precise mode, if tokenizer is jieba
		'''
		if tokenizer == 'jieba':
			self.__tokenized_ret = jieba.cut(self.__text, cut_all)
		elif tokenizer == 'NLPIR':
			# to be implemented
			pass
		else:
			print ('no such tokenizer: %s') %tokenizer

	def del_stop_words(self):
		pass

	def replace_synonym(self):
		pass

	def replace_pronoun(self):
		pass

	def semantic_extend(self):
		'''
		'''
		pass

	def get_result(self):
		'''
		'''
		self.__result = self.__tokenized_ret
		return self.__result


if __name__ == '__main__':
	pro = PreProcessor('在下方输入下方代码后')
	pro.tokenize()
	for string in pro.get_result():
		print string 
