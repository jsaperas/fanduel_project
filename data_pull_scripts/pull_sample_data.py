
# Collect historical data
# This will first collect all players in the NBA with their years played.
# Then, it will look at what players are eligible to be scraped (if they fall within the date range specified)
# Then, for each of those players, we will add in each game they've played.


import requests
import os
import string
import sqlite3
from BeautifulSoup import BeautifulSoup
import data_dump

if __name__=='__main__':
    database = data_dump.data_container()
    query='SELECT * FROM players_stats'
    
    data = database.run_query(query)
    data.to_csv('sample.csv',index=False)
    database.close_connection()
    