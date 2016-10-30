# Script to create database class


class data_container:
	'''
	I think this might have a few parts to it:
	1. Iterate all players in the date ranges, filter ones that dont fall in date range.
	2. For each player pull all of their historical data.
	3. For the update, check for the most recent record, should be today's date, and pull onlly that.
	'''
	def __init__(self, db_name):
		self.db=None
		self.c=None
		self.connect_db(db_name)
		
	def connect_db(self,db_name):
		self.db = sqlite3.connect(db_name)
		self.c = self.db.cursor()
		
	def pull_players(self, table='players_list'):
		query = 'CREATE TABLE IF NOT EXISTS {table} \
		(firstname string, \
		lastname string, \
		pos string, \
		height string, \
		from string, \
		to string, \
		birthdate string, \
		college string )'.format(table)
		
		pass
		
	def pull_stats(self):
		pass
	def update(self):
		pass
	def run_query(self,query):
		self.c = self.db.cursor()
		data = self.c.execute(query)
		
		header = [item[0] for item in data.description]
		data = data.fetchall()
		
		dataset=pd.DataFrame(data = data, columns=header)
		
		return dataset
		
	def close_connection(self):
		self.db.close()
	
	def __repr__(self):
		
		query="SELECT name FROM sqlite_master WHERE type='table';"
		self.c = self.db.cursor()
		tables = self.c.execute(query)
		tables = tables.fetchall()
		
		return 'table names: ' + str(tables)
	
# update data

