import numpy as np
import pandas as pd
import re
import random
from pulp import *
import xlwt

def save_Lineups(lineups):
	writer = pd.ExcelWriter('Line-Ups Test.xlsx')
	lineups.to_excel(writer,'Sheet1')
	writer.save()


def Simulate_Scores(row):
		score = random.gauss(row['Points'],row['Variability'])
		return score


def Optimize_Lineup(df):

	all_players = df['Full Name']
	
	prob = pulp.LpProblem('Line-up',LpMaximize)
	
	players_var = pulp.LpVariable.dicts("Players",all_players,0,1,LpInteger)
	
	total_points = ""
	for r, player in enumerate(all_players):
		formula = players_var[player]*df['Mean/Std'][r]
		total_points += formula

	prob += total_points, "Maximize team total points"

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
	wr =""
	rb =""
	qb =""
	te =""
	d =""
	k =""

	forced_out =""
	for r,player in enumerate(all_players):
			formula = players_var[player]*df['Force Out'][r]
			forced_out += formula
			
	prob += forced_out == 0, ""
	
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

	
#1. Load Data
data = pd.read_csv('player data reduced.csv')
lineups = pd.DataFrame()

#2. Find optimal lineup based on mean/std
optimal_lineup = Optimize_Lineup(data)
lineups['Optimal'] = optimal_lineup	
#for each iteration, remove 1 player from the original lineup and optimize again
		
for i in range(0,9):	
	force_out = optimal_lineup[i]
	data['Force Out'] = data['Full Name'].apply(lambda name: RemovePlayer(name, force_out))
	
	new_lineup = Optimize_Lineup(data)
	lineups['Lineup' + str(i+1)] = new_lineup

print lineups

	
#data['simulation_points'] = data.apply(Simulate_Scores,axis=1)
#print data['simulation_points'][:3] --> this line was used to test the random numbers generated
	
#save_Lineups(lineups)
