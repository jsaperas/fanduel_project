
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


if __name__=='__main__':
    # table names:
    # -----------
    # players_list
    # players_links
    # players_history
    # players_stats
    
	database = data_dump.data_container()
	database.pull_players()
	database.pull_links(2013)
    database.pull_stats(2013)
    database.pull_history(2013)
    database.close_connection()
    
    
    
    # test queries
    query='select * from players_history limit 5'
    database.run_query(query)
    
    query='select * from players_list limit 5'
    database.run_query(query)
    
    query='select * from players_links limit 5'
    database.run_query(query)
