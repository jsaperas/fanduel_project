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
                #    self.
            
        
    def pull_links(self,min_date, table='players_links'):
        # create separate table for just links 
        # map using (name, link, new_link) to merge later
        
        # create links table
        query='CREATE TABLE IF NOT EXISTS {table} \
        ( name string, \
        home_link string, \
        stat_link string, \
        start string, \
        end string)'.format(table=table)
        
        self.c.execute(query)
        self.db.commit()
        
        
        url='http://www.basketball-reference.com/'
        
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
        query='SELECT * FROM {table} where end >= {min_date}'.format(table=table,min_date=min_date)
        
        dataset=self.run_query(query)
        
        list_of_links=dataset.stat_link.values
        list_of_players=dataset.name
        
        n=len(list_of_links)
		
        for j in range(n):
            print 
            url='http://www.basketball-reference.com' 
            url += list_of_links[j]
            
            print 'Starting player {player} with link {link}!'.format(player=list_of_players[j],link=list_of_links[j])
            
            x=requests.get(url)
            y=BeautifulSoup(x.content[700:])
            
            gm=y.findAll('td',attrs={'data-stat':'game_season'})
            date_game=y.findAll('td',attrs={'data-stat':'date_game'})
            age=y.findAll('td',attrs={'data-stat':'age'})
            game_location=y.findAll('td',attrs={'data-stat':'game_location'})
            team_id=y.findAll('td',attrs={'data-stat':'team_id'})
            opp_id=y.findAll('td',attrs={'data-stat':'opp_id'})
            game_result=y.findAll('td',attrs={'data-stat':'game_result'})
            gs=y.findAll('td',attrs={'data-stat':'gs'})
            mp=y.findAll('td',attrs={'data-stat':'mp'})
            fg=y.findAll('td',attrs={'data-stat':'fg'})
            fga=y.findAll('td',attrs={'data-stat':'fga'})
            fg_pct=y.findAll('td',attrs={'data-stat':'fg_pct'})
            fg3_pct=y.findAll('td',attrs={'data-stat':'fg3_pct'})
            fg3a=y.findAll('td',attrs={'data-stat':'fg3a'})
            fta=y.findAll('td',attrs={'data-stat':'fta'})
            ft_pct=y.findAll('td',attrs={'data-stat':'ft_pct'})
            drb=y.findAll('td',attrs={'data-stat':'drb'})
            orb=y.findAll('td',attrs={'data-stat':'orb'})
            trb=y.findAll('td',attrs={'data-stat':'trb'})
            ast=y.findAll('td',attrs={'data-stat':'ast'})
            blk=y.findAll('td',attrs={'data-stat':'blk'})
            stl=y.findAll('td',attrs={'data-stat':'stl'})
            tov=y.findAll('td',attrs={'data-stat':'tov'})
            pf=y.findAll('td',attrs={'data-stat':'pf'})
            pts=y.findAll('td',attrs={'data-stat':'pts'})
            game_score=y.findAll('td',attrs={'data-stat':'game_score'})
            plus_minus=y.findAll('td',attrs={'data-stat':'plus_minus'})
            
            m = len(gm)
            
            for i in range(m):
                print 'starting iteration {i}'.format(i=i)
                # Loop tdrough games
                igm=gm[i]
                idate_game=date_game[i]
                iage=age[i]
                igame_location=game_location[i]
                iteam_id=team_id[i]
                iopp_id=opp_id[i]
                igame_result=game_result[i]
                igs=gs[i]
                imp=mp[i]
                ifg=fg[i]
                ifga=fga[i]
                ifg_pct=fg_pct[i]
                ifg3_pct=fg3_pct[i]
                ifg3a=fg3a[i]
                ifta=fta[i]
                ift_pct=ft_pct[i]
                idrb=drb[i]
                iorb=orb[i]
                itrb=trb[i]
                iast=ast[i]
                iblk=blk[i]
                istl=stl[i]
                itov=tov[i]
                ipf=pf[i]
                ipts=pts[i]
                igame_score=game_score[i]
                iplus_minus=plus_minus[i]
            
            
            
    def run_query(self,query):
        #self.c = self.db.cursor()
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

