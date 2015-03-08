import pymysql

class WrapItUp:

	_connection = None
	_defaultCursor = None
	_cursors = {}

	def __init__(self, username='', password='', socket='', ip='', database='', timeout = 20):

		if socket != '':
			try:
				self._connection = pymysql.connect(unix_socket=socket, user=username, passwd=password, db=database, connect_timeout = timeout)
				self._connection.autocommit(True) #Saves us a headache with having to run .commit() after every insert query.
				#print('connection established via sockets!')
				self._defaultCursor = self._connection.cursor()
			except:
				print('Unable to establish connection via sockets')
		elif socket == '' and ip != '':
			try:
				self._connection = pymysql.connect(host=ip, user=username, passwd=password, db=database, port=3306, connect_timeout = timeout)
				self._connection.autocommit(True)
				#print('connection established by ip!')
				self._defaultCursor = self._connection.cursor()
			except:
				print('Unable to establish connection via IP')
		else:
			print('Unable to create any mysql connection, halp!')
			return


	#Allows custom cursor creation if required. Runs based off the class connection that exists at the time.
	def CreateCursor(self, stringName):
		if self.cursor['stringName']:
			return
		self._cursors['stringName'] = self._connection.cursor()


	#Explicit class to check whether or not a cursor exists. Does not work for default cursor as always presumed
	#to exist.	
	def GetValidCursor(self,stringName):
		if self.cursor['stringName']:
			return True
		else:
			return False

	#Same as above technically but will return the cursor object
	def GetCursor(self,stringName):
		if self._cursors['stringName']:
			return self._cursors['stringName']
		else:
			return None

	'''
		Generic query function that takes an input query, a tuple of arguments (regardless of type)
			- Can return via itself or via a callback function (offload or subject to another process)
			- Will use the default class cursor to provide a slightly better interaction for dev purposes
			- Can use a different cursor if required
			- Doesn't technially catch sql specific arguments only yet, should do but oh well.
	'''
	def Query(self, stringQuery, *tupleArguments, callbackFunction=None, cursor=None, single=False):
		#Allow for another cursor to be used here if required for io performance. Cursors techniaclly queue up queries.

		if self._connection == None:
			return False

		if cursor == None:
			cursor = self._defaultCursor

		print(*tupleArguments)

		try:
			cursor.execute(stringQuery, *tupleArguments)
		except Exception as error:
			print('MYSQL Error: ' + str(error))

		if single == True:
			results = cursor.fetchone()
		else:
			results = cursor.fetchall()

		#if we want to jump out and pass the results to say, a generic handler, we can do this.
		if callbackFunction != None:
			callbackFunction(results)
		else:
			return results


	#Closes the default connection and cursors only.
	def CloseConnection(self):
		self._defaultCursor.close()
		self._connection.close()



