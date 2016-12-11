import numpy as np
import pandas as pd
import re
import random
from pulp import *
import xlwt

def save_Lineups(lineups):
	writer = pd.ExcelWriter('Line-Ups Points.xlsx')
	lineups.to_excel(writer,'Sheet1')
	writer.save()


def Optimize_Lineup(df):

	all_players = df['player_name']
	
	prob = pulp.LpProblem('Line-up',LpMaximize)
	
	players_var = pulp.LpVariable.dicts("Players",all_players,0,1,LpInteger)

	metric = 'Predicted_Points'
	metric_2 = 'STD_10'
	
	total_points = ""
	for r, player in enumerate(all_players):

		#This line is the key to define what we are optimizing on
		#In this case, we are optimizing on points only (no stdev yet) as defined by metric
		formula = players_var[player]*(df[metric][r]-df[metric_2][r])
		total_points += formula

	prob += total_points, "Maximize team total predicted points"

	# Add constraints
	salary_cap = 60000
	total_salary =""
	
	#salary constraint
	for r,player in enumerate(all_players):
			formula = players_var[player]*df['Salary'][r]
			total_salary += formula
			
	prob += (total_salary <= salary_cap), ""
	
	
	#Not a constraint. Just to calculate expected score
	expected_score =""
	for r,player in enumerate(all_players):
			formula = players_var[player]*df['Points'][r]
			expected_score += formula
	
	#Add position constraints
	pg =""
	sg =""
	sf =""
	pf =""
	c =""

	forced_out =""
	for r,player in enumerate(all_players):
			formula = players_var[player]*df['Force Out'][r]
			forced_out += formula
			
	prob += forced_out == 0, ""
	
	for r,player in enumerate(all_players):
		if df['Position'][r] == "PG":
			pg += players_var[player]
		elif df['Position'][r] == "SG":
			sg += players_var[player]
		elif df['Position'][r] == "SF":
			sf += players_var[player]
		elif df['Position'][r] == "PF":
			pf += players_var[player]
		elif df['Position'][r] == "C":
			c += players_var[player]

	prob += pg == 2, ""
	prob += sg == 2, ""
	prob += sf == 2, ""
	prob += pf == 2, ""
	prob += c == 1, ""

	
	line_up = prob.solve()
	assert line_up == pulp.LpStatusOptimal
	
	lineup = []
	for player in all_players:
		if value(players_var[player]) == 1:
			lineup.append(player)
	lineup.append(value(expected_score))
	lineup.append(value(total_salary))
	return pd.Series(lineup)				
	
def RemovePlayer(name, fo_name):
	if name == fo_name:
		return 1
	else:
		return 0


#Main script

#1. Load Data

directory = '../data/'
data = pd.read_csv(directory + 'player_list_example.csv')
lineups = pd.DataFrame()

#2. Find optimal lineup based on the metric selected
optimal_lineup = Optimize_Lineup(data)
lineups['Optimal'] = optimal_lineup	

#For each iteration, remove 1 player from the original lineup and optimize again		
for i in range(0,9):	
	force_out = optimal_lineup[i]
	data['Force Out'] = data['player_name'].apply(lambda name: RemovePlayer(name, force_out))
	
	new_lineup = Optimize_Lineup(data)
	lineups['Lineup' + str(i+1)] = new_lineup

data['simulation_points'] = data.apply(Simulate_Scores,axis=1)
save_Lineups(lineups)
