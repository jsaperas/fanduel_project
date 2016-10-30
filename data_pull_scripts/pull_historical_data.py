
# Collect historical data
# In the future we want to collect injury reports 
# Also want to collect more data 

import requests
import os
import string
import sqlite3
from BeautifulSoup import BeautifulSoup
import data_dump

dir='c://Users/James//Desktop//fanduel_project'
os.chdir(dir)



########################################################################################################
# params

# Loop a-z
alphabet=string.lowercase
for letter in alphabet:

url='http://www.basketball-reference.com/players/{alpha}/'.format(alpha=alphabet[0])

x=requests.get(url)
#x=urllib2.urlopen(url)

# This doesnt parse correctly unless we look at strings after 700
y=BeautifulSoup(x.content[700:])

list_of_players=y.findAll('th',attrs={'data-stat':'player'})

# ignore the first row since it's a header
n = len(list_of_players)

for player in range(1,n):
	
	player_name = list_of_players[player].text
	link = list_of_players[player].next['href']
	
	# stats information
	player_bio = list_of_players[player].findNextSiblings()
	# should have 7 fields: min year, max year, position, height, weight, birthdate, college
	m = len(player_bio)
	
	if(m != 7): 
		print 'error, wrong player bio length!'
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
	#self.c.executemany(query,data)
	#self.db.commit()
	

years=[
		'2017', # current year
		'2016',
		'2015',
		'2014',
		'2013'
]

east=[
		'ATL',
		'CHI',
		'CHO', 
		'CLE', 
		'TOR', 
		'MIA', 
		'IND', 
		'DET', 
		'BOS', 
		'BRK', 
		'WAS', 
		'PHI', 
		'ORL', 
		'NYK', 
		'MIL' 
]

west=[
		'MEM', 
		'SAS', 
		'DEN', 
		'OKC', 
		'LAC', 
		'HOU', 
		'UTA', 
		'GSW', 
		'LAL', 
		'SAC', 
		'POR', 
		'PHO', 
		'MIN', 
		'DAL', 
		'NOP' 
]

