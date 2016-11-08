import numpy as np
import pandas as pd
import re
import random
from pulp import *
import xlwt
from tqdm import tqdm

def save_Lineups(lineups):
	writer = pd.ExcelWriter('Line-Ups Reduced.xlsx')
	lineups.to_excel(writer,'Sheet1')
	writer.save()


def Simulate_Scores(row):
		score = random.gauss(row['Points'],row['Variability'])
		return score


def Optimize_Lineup(df):

	all_players = df['Full Name']
	
	#Create problems and variables
	prob = pulp.LpProblem('Line-up',LpMaximize)
	players_var = pulp.LpVariable.dicts("Players",all_players,0,1,LpInteger)
	
	#Create objective function to maximize points
	total_points = ""
	for r, player in enumerate(all_players):
		formula = players_var[player]*df['simulation_points'][r]
		total_points += formula
	prob += total_points, "Maximize team total points"

	# Add salary constraints
	salary_cap = 60000
	total_salary =""
	for r,player in enumerate(all_players):
			formula = players_var[player]*df['Salary'][r]
			total_salary += formula
	prob += (total_salary <= salary_cap), ""
	
	#Add position constraints
	wr =""
	rb =""
	qb =""
	te =""
	d =""
	k =""

	for r,player in enumerate(all_players):
		if df['Position'][r] == "WR":
			wr += players_var[player]
		elif df['Position'][r] == "RB":
			rb += players_var[player]
		elif df['Position'][r] == "QB":
			qb += players_var[player]
		elif df['Position'][r] == "K":
			k += players_var[player]
		elif df['Position'][r] == "TE":
			te += players_var[player]
		else:
			d += players_var[player]

	prob += wr == 3, ""
	prob += rb == 2, ""
	prob += qb == 1, ""
	prob += te == 1, ""
	prob += k == 1, ""
	prob += d == 1, ""


	line_up = prob.solve()
	assert line_up == pulp.LpStatusOptimal
	
	
	
	lineup = np.array([])
	for player in all_players:
		if value(players_var[player]) == 1:
			
			lineup = np.append(lineup,player)
	lineup = np.append(lineup,value(prob.objective))
	lineup = np.append(lineup,value(total_salary))
	return lineup				
	

	
#1. Read data into pandas DataFrame
data = pd.read_csv('player data reduced.csv')

lineups = []

#2. Iterate
for i in tqdm(range(1,20000)):
	
	#2.1 Simulate player scores
	data['simulation_points'] = data.apply(Simulate_Scores,axis=1)
	
	#2.2 Optimize_Lineup
	new_lineup = Optimize_Lineup(data)
	lineups.append(new_lineup)

#Saves lineups in an Excel file	
lineups = pd.DataFrame(lineups,columns=['P1','P2','P3','P4','P5','P6','P7','P8','P9','Score','Salary'])
save_Lineups(lineups)



