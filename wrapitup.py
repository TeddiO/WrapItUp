import pymysql

class WrapItUp:

	_connection = None
	_defaultCursor = None
	cursors = {
		'Cursor' : pymysql.cursors.Cursor,
		'DictCursor' : pymysql.cursors.DictCursor,
		'SSCursor' : pymysql.cursors.SSCursor,
		'SSDictCursor' : pymysql.cursors.SSDictCursor
	}

	def __init__(self, username=None, password=None, socket=None, host=None, database=None, timeout = 20, autocommit=True, charset="utf8mb4"):

		self._customCursors = {} #Create this here to prevent it being shared.

		if socket is not None and host is not None:
			raise Exception("Both socket and ip are set. Use one or the other!")

		try:
			self._connection = pymysql.connect(unix_socket=socket, host=host, user=username, passwd=password, db=database, connect_timeout = timeout, charset=charset)
			self._connection.autocommit(autocommit) #Saves us a headache with having to run .commit() after every insert query.
			self._defaultCursor = self._connection.cursor()
		except Exception as Error:
			raise Error


	def CreateCursor(self, stringName, cursorType=pymysql.cursors.Cursor):
		#Allows custom cursor creation if required. Runs based off the class connection that exists at the time.
		'''
		Cursors available -
			- Cursor
			- DictCursor
			- SSCursor
			- SSDictCursor

			- If you import pymysql directly into your file, you can use other available cursors.
		'''
		if stringName in self._customCursors:
			return False
			
		self._customCursors[stringName] = self._connection.cursor(cursorType)

		return self._customCursors[stringName]


	#Explicit class to check whether or not a cursor exists. Does not work for default cursor as always presumed
	#to exist.
	def GetValidCursor(self, stringName):
		if stringName in self._customCursors:
			return True
		else:
			return False

	#Same as above technically but will return the cursor object
	def GetCursor(self, stringName):
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
	def Query(self, stringQuery, *tupleArguments, callbackFunction=None, cursor=None, single=False):
		#Allow for another cursor to be used here if required for io performance. Cursors techniaclly queue up queries.

		if self._connection is None:
			return False

		cursor = cursor or self._defaultCursor

		try:
			cursor.execute(stringQuery, *tupleArguments)
		except Exception as error:
			print('MYSQL Error: ' + str(error))

		if single is True:
			results = cursor.fetchone()
		else:
			results = cursor.fetchall()

		#if we want to jump out and pass the results to say, a generic handler, we can do this.
		if callbackFunction is not None:
			callbackFunction(results)
		else:
			return results

			

	#Closes the default connection and cursors only.
	def CloseConnection(self):
		for cursor in self._customCursors.values():
			cursor.close()

		self._defaultCursor.close()
		self._connection.close()



