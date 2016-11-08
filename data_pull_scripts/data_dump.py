# Script to create database class
import sqlite3
import time
import string
import requests
import os
import numpy as np 
import pandas as pd
from BeautifulSoup import BeautifulSoup


class data_container():
	'''
	I think this might have a few parts to it:
	1. Iterate all players in the date ranges, filter ones that dont fall in date range.
	2. For each player pull all of their historical data.
	3. For the update, check for the most recent record, should be today's date, and pull onlly that.
	'''
	def __init__(self, db_name='fanduel.db'):
		self.db=None
		self.c=None
		self.connect_db(db_name)
		
	def connect_db(self,db_name):
		self.db = sqlite3.connect(db_name)
		self.c = self.db.cursor()
		
	def pull_players(self, table='players_list'):
		query = 'CREATE TABLE IF NOT EXISTS {table} \
		(name string, \
		link string, \
		pos string, \
		height string, \
		weight string, \
		start string, \
		end string, \
		birthdate string, \
		college string )'.format(table=table)
		
		self.c.execute(query)
		self.db.commit()
		
		counter=0
		
		# Loop a-z
		#alphabet=string.lowercase
		alphabet='a'
		
		n_alpha=len(alphabet)
		for letter in range(n_alpha):
			counter += 1
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
				if list_of_players[player].next.has_key('href'):
					link = list_of_players[player].next['href']
				else:
					print 'error, link does not exist for {player}!'.format(player=player_name)
					link=''
					
				# stats information
				player_bio = list_of_players[player].findNextSiblings()
				# should have 7 fields: min year, max year, position, height, weight, birthdate, college
				m = len(player_bio)
				
				if(m != 7): 
					print 'error, wrong player bio length for {player}!'.format(player=player_name)
					year_min=''
					year_max=''
					pos=''
					height=''
					weight=''
					birth_date=''
					college_name=''
					data=(player_name,link,pos,height,weight,year_min,year_max,birth_date,college_name)
				
				else:
					year_min=player_bio[0].text
					year_max=player_bio[1].text
					pos=player_bio[2].text
					height=player_bio[3].text
					weight=player_bio[4].text
					birth_date=player_bio[5].text
					college_name=player_bio[6].text
					data=(player_name,link,pos,height,weight,year_min,year_max,birth_date,college_name)
				
				print data
				query='INSERT INTO {table} VALUES ('.format(table=table)
				query += ','.join((m+2)*'?') + ')'
				self.c.execute(query,data)
				self.db.commit()
				#if counter % 10==0:
				#	self.
			
		
	def pull_stats(self, min_date):
		# create separate table for just links 
		# map using (name, link, new_link) to merge later
		url='http://www.basketball-reference.com/'
		
		query='SELECT * FROM player_list where end >= {min_date}'.format(min_date)
		player_stats=self.run_query(query)
		
		links=player_stats.link
		players=player_stats.name
		
		n = player_stats.shape[0]
		for i in range(n):
			if links[i] == '':
				print 'player {player} does not have a valid link!'.format(player=players[i])
				continue
			url += links[i]
			x=requests.get(url)
			y=BeautifulSoup(x.content)
			
			list_of_seasons=y.findAll('a')
			
			for season in list_of_seasons:
				if season.get('href'):
					link =  season.get('href')
					if 'gamelog' in link:
						list_of_links.append(link) 
					
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

