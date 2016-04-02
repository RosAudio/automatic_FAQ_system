# encoding=utf-8
from __future__ import division
from multiprocessing import Pool,Queue
import multiprocessing
import math
import numpy
import mysql_executer

class Matcher(object):
	def __init__(self,question,update = False):
		'''
		'''
		if update == True:
			'''
			update pos, words 
			'''
			pass
		else:
			pass

		self.__question = question
		self.__sentence = {} # dict for questions in the database with same words to the question
		self.__sliced_sentence #sliced sorted sentence

		self.__pos # need to initialize and update
		self.__words = {'word1':[pos[0],pos[1],pos[2]],'word2':[pos[0],pos[1],pos[3]]} # need to initialize and update

	def select_candidate(self, ratio=0.5):
		'''
		search and get questions in the database with most same words to the question 
		param@ ratio: the percentage of questions in the database 
		return: positions of sentences with the most same words to the target question
		'''
		for w in self.__question:
			if w in self.__words:
				word_list = self.__words[w]
				for pos in word_list:
					if pos not in self.__sentence:
						self.__sentence[pos] = 0
					self.__sentence[pos] += 1
			else:
				'''
				to be implemented !!!
				if the word is not in the dict of words, add this word to the dict, update database, etc.
				'''
				pass

		sorted_sentence = sorted(self.__sentence.iteritems(),key = lambda __sentence : self.__sentence[1],reverse = True) # return a list of tuples
		num = math.ceil(ratio*len(sorted_sentence)) 
		self.__sliced_sentence = sorted_sentence[:num]
		return self.__sliced_sentence

	def get_answer(self,question,ques_ans,mode):
		'''
		get the best answer in the database
		param@ question: target question
		param@ ques_ans: list of question-answers in the database, [[pos1,q1,a1],[pos2,q2,a2]] 
		param@ mode: a tuple of a similarity algorithm name and threshold, eg: ('TFIDF',0.8)
		return: the answer with the largest similarity >= threshold
		'''
		MODE = ['TFIDF',''] 
		if mode[0] not in MODE: # cheack if mode is avaiable
			print ('no such mode: %s.') %mode
			return None
		if mode[0] == 'TFIDF':
			pool = Pool(5) # create a process pool
			manager = multiprocessing.Manager()
			queue = manager.Queue()
			lock = manager.Lock()
			M = len(self.__words)
			for ques in ques_ans:
				pool.apply_async(tfidf,args=(question,ques,M,queue,lock))
			pool.close()
			pool.join()
			# get all elements in the queue, element (question,similarity)
			answer = []
			while not queue.empty():
				answer.append(queue.get())
			sorted_ans = sorted(answer,key = lambda x : x[1],reverse=True)
			# get the answers which similarity > threshold
			ans = [element[0][2] for element in sorted_ans, if element[1] >= threshold] 
			return ans[0]

		elif mode == '':
			# to be implemented
			pass	

	
	def single_process_tfidf(self,ques_ans):
		'''
		calculate similarity using TFIDF algorithm
		param@ ques_ans: list of question-answers in database,[[pos1,q1,a1],[pos2,q2,a2]] 
		'''

		'''
		replace "for pos in ..." with multiprocessing or multithreads
		'''
		T = [] # vector list of question in database
		M = len(self.__words)
		for question in ques_ans:
			# n = [] # the occurence in the question of a certain word
			# m = [] # the number of questions with the certain word in the FAQ database
			t = [] # vector of a question  
			for word in ques_ans:
				ni = ques_ans.count(word) # the occurence in the question of word
				mi = len(self.__words[word]) + 1 # the number of questions with word in the FAQ database, in case of no such word in database
				ti = ni * math.log(M/mi) # TF * IDF
				t.append(ti)
			T.append(t)
		return T


	def tfidf(self,ques_target,question,M,queue,lock):
		'''
		calculate the similarity between the target question and a question in the database
		param@ ques_target: a target question, [w1,w2,w3]
		param@ question: a question-answer, [pos1,q1,a1]
		param@ M: the number of all the questions in the database
		param@ queue: queue for similarity
		param@ lock: processing lock
		'''
		lock.acquire()
		t = [] # vector of a question in the database
		t_tar =[] # vector of a target question
		for word in ques_target:
			ni = question[1].count(word)
			ni_tar = ques_target.count(word)
			mi = len(self.__words[word]) + 1
			ti = ni * math.log(M/mi)
			ti_tar = ni_tar * math.log(M/mi)
			t.append(ti)
			t_tar.append(ti_tar)
		# calculate the similarity
		t_arr = numpy.array(t)
		t_tar_arr = numpy.array(t_tar)
		l_t = numpy.sqrt(t_arr.dot(t_arr))
		l_t_tar = numpy.sqrt(t_tar_arr.dot(t_tar_arr))
		similarity = t_arr.dot(t_tar_arr)/(l_t * l_t_tar)
		# put (question,similarity) into queue
		queue.put((question,similarity))
		lock.release()


if __name__ == '__main__':
	d = {'one':1,'two':2,'three':3}
	print sorted(d.iteritems(),key = lambda d:d[1],reverse = True)
	num = 2.3
	print math.ceil(num)
	'''
	# test multiprocess, queue
	def add2queue(name,q,lock):
		lock.acquire()
		q.put(name)
		for i in range(10):
			q.put(i)
		lock.release()

	pool = Pool(2) # create a process pool
	manager = multiprocessing.Manager()
	queue = manager.Queue()
	lock = manager.Lock()
	for i in range(5):
		pool.apply_async(add2queue,args=(i*100,queue,lock))
	pool.close()
	pool.join()

	l = []
	while not queue.empty():
		l.append(queue.get())
	print l
	'''
	ans = [(0.1,'a'),(0.3,'b'),(0.4,'c'),(0.5,'d')]
	print sorted(ans,key = lambda y:y[0])






