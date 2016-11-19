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
        
    def pull_team_stats(self):
        pass
    
    
    def pull_players(self, table='players_list'):
        
        query='DROP TABLE IF EXISTS players_list'
        
        
        self.c.execute(query)
        self.db.commit()
        
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
        alphabet=string.lowercase
        #alphabet='a'
        
        n_alpha=len(alphabet)
        for letter in range(n_alpha):
            
            print 'pulling for letters {letter}!'.format(letter=alphabet[letter])
            
            counter += 1
            url='http://www.basketball-reference.com/players/{alpha}/'.format(alpha=alphabet[letter])

            x=requests.get(url)

            # This doesnt parse correctly unless we look at strings after 700
            y=BeautifulSoup(x.content[700:])

            list_of_players=y.findAll('th',attrs={'data-stat':'player'})

            # ignore the first row since it's a header
            n = len(list_of_players)

            # iterate through all players and store their names
            for iplayer in range(1,n):
                
                player_name = list_of_players[iplayer].text
                print 'pulling player {player}!'.format(player=player_name)
                
                if list_of_players[iplayer].next.get('href'):
                    link = list_of_players[iplayer].next['href']
                elif list_of_players[iplayer].next.next.get('href'):
                    link = list_of_players[iplayer].next.next['href']
                else:
                    print 'error, link does not exist for {player}!'.format(player=player_name)
                    link=''
                    
                # stats information
                player_bio = list_of_players[iplayer].findNextSiblings()
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
                
                #print data
                query='INSERT INTO {table} VALUES ('.format(table=table)
                query += ','.join((m+2)*'?') + ')'
                self.c.execute(query,data)
                self.db.commit()
                #if counter % 10==0:
                #    self.
            
        
    def pull_links(self,min_date, table='players_links'):
        # create separate table for just links 
        # map using (name, link, new_link) to merge later
        
        query='DROP TABLE {table}'.format(table=table)
        
        self.c.execute(query)
        self.db.commit()
        
        # create links table
        query='CREATE TABLE IF NOT EXISTS {table} \
        ( name string, \
        home_link string, \
        stat_link string, \
        start string, \
        end string)'.format(table=table)
        
        self.c.execute(query)
        self.db.commit()
        
        
        
        # select only eligible players
        query='SELECT * FROM players_list where end >= {date}'.format(date=min_date)
        player_stats=self.run_query(query)
        
        links=player_stats.link
        players=player_stats.name
        start=player_stats.start
        end=player_stats.end
		
        n = player_stats.shape[0]
        for i in range(n):
            if links[i] == '':
                print 'player {player} does not have a valid link!'.format(player=players[i])
                continue
				
			#print 'Success! player {player} has a valid link!'.format(player=players[i])
            print 'Success! player {player} has a valid link!'.format(player=players[i])
            url='http://www.basketball-reference.com/'
            url += links[i]
            x=requests.get(url)
            y=BeautifulSoup(x.content[700:])
            
            list_of_seasons=y.findAll('a')
            list_of_inputs=[]
			
            for season in list_of_seasons:
                if season.get('href'):
                    link =  season.get('href').rstrip('/')
                    if 'gamelog' in link:
                        input=(players[i],links[i],link,str(start[i]),str(end[i]))
                        list_of_inputs.append(input)
            
            list_of_inputs=set(list_of_inputs)
            list_of_inputs=list(list_of_inputs)
            
            # remove duplicates
            m = 5
            
            # add to db
            query='INSERT INTO {table} VALUES ('.format(table=table)
            query += ','.join((m)*'?') + ')'
            print list_of_inputs
            self.c.executemany(query,list_of_inputs)
            self.db.commit()
            
            
    def pull_stats(self, min_date, table='players_links'):
        
        # pull gamelog links for all eligible players
        query='SELECT * FROM {table} where start >= {min_date}'.format(table=table,min_date=min_date)
        
        dataset=self.run_query(query)
        
        list_of_links=dataset.stat_link.values
        list_of_players=dataset.name
        
        n=len(list_of_links)
		
        
		# create new table
        query='DROP TABLE players_stats'
        self.c.execute(query)
        self.db.commit()
        
        query='CREATE TABLE players_stats \
        (player_name string, \
         game_season string, \
         date_game string, \
         age string, \
         team_id string, \
         location string, \
         opp_id string, \
         game_result string, \
         gs string, \
         mp string, \
         fg string, \
         fga string, \
         fg_pct string, \
         fg3 string, \
         fg3a string, \
         fg3_pct string, \
         ft string, \
         fta string, \
         ft_pct string, \
         orb string, \
         drb string, \
         trb string, \
         ast string, \
         stl string, \
         blk string, \
         tov string, \
         pf string, \
         pts string, \
         game_score string, \
         plus_minus string, \
         reason_code string )'
         
         
        self.c.execute(query)
        self.db.commit()
        
        for j in range(n):
            print 
            url='http://www.basketball-reference.com' 
            url += list_of_links[j]
            
            print 'Starting player {player} with link {link}!'.format(player=list_of_players[j],link=list_of_links[j])
            
            x=requests.get(url)
            y=BeautifulSoup(x.content[700:])
            
            values=y.findAll('th',attrs={'data-stat':'ranker'})
            
            m = len(values)
            
            # loop through players
            player_game_stats=[]
            for i in range(1,m):
                #print 'starting iteration {i}'.format(i=i)
				
                ivalue=values[i].findNextSiblings()
                
                # check to see if it has all values
                if len(ivalue)!=29:
                    print 'error game {iter} does not have complete values!'.format(iter=i)
                    reason_code=ivalue[len(ivalue)-1].text
                    print reason_code
                else:
                    reson_code='complete'
                o = len(ivalue)
                
                
                list_of_gamestat=[list_of_players[j]]
                
                for k in range(o):
                    list_of_gamestat.append(ivalue[k].text)
                
                len_gs=len(list_of_gamestat)
                if len_gs !=30:
                    for k in range(30-len_gs):
                        list_of_gamestat.append('')
                
                list_of_gamestat.append(reson_code)
                
                list_of_gamestat=tuple(list_of_gamestat)
                player_game_stats.append(list_of_gamestat)
                #print len(list_of_gamestat)
            
            query='INSERT INTO players_stats VALUES ('
            query += ','.join((31)*'?') + ')'
            #print player_game_stats
            self.c.executemany(query,player_game_stats)
            self.db.commit()
            
    def run_query(self,query):
        #self.c = self.db.cursor()
        data = self.c.execute(query)
        
        header = [item[0] for item in data.description]
        data = data.fetchall()
        
        dataset=pd.DataFrame(data = data, columns=header)
        
        return dataset
    
    def update_stats(self,current_year=2017):
        # pull list of current players
        query='SELECT * FROM players_links WHERE end = {current_year}'.format(current_year=current_year)
        
        dataset=self.run_query(query)
        
        list_of_links=dataset.stat_link.values
        list_of_players=dataset.name
        
        n=len(list_of_links)
        
        # remove current values
        query='DELETE FROM players_stats where end={current_year}'.format(current_year=current_year)
        
        self.c.execute(query)
        self.db.commit()
        
        # loop through players
        for j in range(n):
            print 
            url='http://www.basketball-reference.com' 
            url += list_of_links[j]
            
            print 'Starting player {player} with link {link}!'.format(player=list_of_players[j],link=list_of_links[j])
            
            x=requests.get(url)
            y=BeautifulSoup(x.content[700:])
            
            values=y.findAll('th',attrs={'data-stat':'ranker'})
            
            m = len(values)
            
            # loop through players
            player_game_stats=[]
            for i in range(1,m):
                #print 'starting iteration {i}'.format(i=i)
				
                ivalue=values[i].findNextSiblings()
                
                # check to see if it has all values
                if len(ivalue)!=29:
                    print 'error game {iter} does not have complete values!'.format(iter=i)
                    reason_code=ivalue[len(ivalue)-1].text
                    print reason_code
                    
                else:
                    reson_code='complete'
                o = len(ivalue)
                
                
                list_of_gamestat=[list_of_players[j]]
                
                for k in range(o):
                    list_of_gamestat.append(ivalue[k].text)
                
                len_gs=len(list_of_gamestat)
                if len_gs !=30:
                    for k in range(30-len_gs):
                        list_of_gamestat.append('')
                
                list_of_gamestat.append(reson_code)
                
                list_of_gamestat=tuple(list_of_gamestat)
                player_game_stats.append(list_of_gamestat)
                #print len(list_of_gamestat)
            
            query='INSERT INTO players_stats VALUES ('
            query += ','.join((31)*'?') + ')'
            #print player_game_stats
            self.c.executemany(query,player_game_stats)
            self.db.commit()
            
    def close_connection(self):
        self.db.close()
    
    def __repr__(self):
        
        query="SELECT name FROM sqlite_master WHERE type='table';"
        self.c = self.db.cursor()
        tables = self.c.execute(query)
        tables = tables.fetchall()
        
        return 'table names: ' + str(tables)
    
# update data

