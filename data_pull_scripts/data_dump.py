# Script to create database class
import sqlite3
import time


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
	
		# Loop a-z
		alphabet=string.lowercase
		for letter in alphabet:
		
			url='http://www.basketball-reference.com/players/{alpha}/'.format(alpha=alphabet[letter])

			x=requests.get(url)

			# This doesnt parse correctly unless we look at strings after 700
			y=BeautifulSoup(x.content[700:])

			list_of_players=y.findAll('th',attrs={'data-stat':'player'})

			# ignore the first row since it's a header
			n = len(list_of_players)

			# iterate through all players and store their names
			for player in range(1,n):

				player_name = list_of_players[player].text
				link = list_of_players[player].next['href']
				
				# stats information
				player_bio = list_of_players[player].findNextSiblings()
				# should have 7 fields: min year, max year, position, height, weight, birthdate, college
				m = len(player_bio)
				
				if(m != 7): 
					print 'error, wrong player bio length for {player}!'.format(player=player_name)
					continue
				else:
					year_min=player_bio[0].text
					year_max=player_bio[1].text
					pos=player_bio[2].text
					height=player_bio[3].text
					weight=player_bio[4].text
					birth_date=player_bio[5].text
					college_name=player_bio[6].text
					data=(year_min,year_max,pos,height,weight,birth_date,college_name)
					
				query='INSERT INTO {table} VALUES ('.format(table)
				query += ','.join(m*'?' + ')'
				self.c.executemany(query,data)
				self.db.commit()
			
		
	def pull_stats(self, date_range):
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

