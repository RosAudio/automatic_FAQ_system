# encoding=utf-8

try:
	import mysql.connector
except e:
	print ('Error: %s') %e

class MySQL_Executer(object):
	'''
	MySQL wrapper
	'''
	def __init__(self, user, password, database):
		try:
			self.__connect = mysql.connector.connect(user=user, password=password, database=database)
			self.__cursor = self.__connect.cursor()
		except e:
			print ('MySQL connection error: %s') %e
		
	def create_table(self):
		'''
		to be implemented !!!
		'''
		self.__cursor.execute('select %s from where ')

	def insert_record(self,record):
		'''
		insert a record into database
		param@ record: a tuple of a record's size and a segmented record. eg: (10, 'question answer')
		'''
		self.__cursor.execute()

	def query(self,pos):
		pos = pos
		self.__cursor.execute()
		# question is list of words
		result = [pos,question,answer]
		return result 

	def delete_record(self):
		self.__cursor.execute()

	def update(self):
		pass

	def close(self):
		self.__cursor.close()


if __name__ == '__main__':
	'''
	MySQL_Executer test
	to be implemented !!!
	'''
	pass


