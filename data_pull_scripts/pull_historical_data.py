
# Collect historical data
# In the future we want to collect injury reports 
# Also want to collect more data 

import requests
import os
import string

dir='c://Users/James//Desktop//fanduel_project'
os.chdir(dir)



########################################################################################################
# params

# Loop a-z
alphabet=string.lowercase

url='http://www.basketball-reference.com/players/{alpha}/'.format(alpha=alphabet[0])


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


class data_container:
	'''
	I think this might have a few parts to it:
	1. Iterate all players in the date ranges, filter ones that dont fall in date range.
	2. For each player pull all of their historical data.
	3. For the update, check for the most recent record, should be today's date, and pull onlly that.
	'''
	def __init__(self):
		pass
	

# update data

