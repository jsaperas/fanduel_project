
# Collect historical data
# This will first collect all players in the NBA with their years played.
# Then, it will look at what players are eligible to be scraped (if they fall within the date range specified)
# Then, for each of those players, we will add in each game they've played.


import requests
import os
dir='c://Users/James//Desktop//fanduel_project/data_pull_scripts'
os.chdir(dir)


import string
import sqlite3
from BeautifulSoup import BeautifulSoup
import data_dump




########################################################################################################
# params
	

date_range={
		'max_date' : '2017', # current year
		'min_date' : '2013'
}


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

if __name__=='__main__':
	database = data_dump.data_container()
	database.pull_players()
	database.pull_links(2014)
	database.pull_stats(2014)
	database.close_connection()