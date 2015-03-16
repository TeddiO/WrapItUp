import pymysql

class WrapItUp:

	_connection = None
	_defaultCursor = None
	_customCursors = {}
	cursors = {
		'Cursor' : pymysql.cursors.Cursor,
		'DictCursor' : pymysql.cursors.DictCursor,
		'SSCursor' : pymysql.cursors.SSCursor, 
		'SSDictCursor' : pymysql.cursors.SSDictCursor
	}

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
	'''
		Cursors available - 
			- Cursor
			- DictCursor
			- SSCursor
			- SSDictCursor

			- If you import pymysql directly into your file, you can use other available cursors.
	'''
	def CreateCursor(self, stringName, type=pymysql.cursors.Cursor):
		if stringName in self._customCursors:
			return False
			
		self._customCursors[stringName] = self._connection.cursor(type)

		return self._customCursors[stringName]


	#Explicit class to check whether or not a cursor exists. Does not work for default cursor as always presumed
	#to exist.	
	def GetValidCursor(self,stringName):
		if stringName in self._customCursors:
			return True
		else:
			return False

	#Same as above technically but will return the cursor object
	def GetCursor(self,stringName):
		if stringName in self._customCursors:
			return self._customCursors[stringName]
		else:
			return None

	'''
		Generic query function that takes an input query, a tuple of arguments (regardless of type)
			- Can return via itself or via a callback function (offload or subject to another process)
			- Will use the default class cursor to provide a slightly better interaction for dev purposes
			- Can use a different cursor if required
			- Doesn't technially catch sql specific arguments only yet, should do but oh well.
	'''
	def Query(self, stringQuery, *tupleArguments, callbackFunction=None, cursor=_defaultCursor, single=False):
		#Allow for another cursor to be used here if required for io performance. Cursors techniaclly queue up queries.

		if self._connection == None:
			return False

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
		for cursor in self._customCursors:
			cursor.close()

		self._defaultCursor.close()
		self._connection.close()



