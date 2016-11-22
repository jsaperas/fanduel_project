## Overview

This section will contain the scripts for the data pull.  The source we are pulling from now is basketball-reference.com.


### Database
The main database is fanduel.db and the tables are:
- players_list - this contains the list of players pulled by the database along with their player link and basic stats.
- players_links - this has the links for each season each player has played in.  There is a one-to-many mapping from players_list to players_links.
- players_stats - this table contains the game-by-game stats for each player.  This again has a one-to-many mapping from the previous table.  There are 29 stats collected but in the future we may want to collect more.


to pull from the table, here is an example query.  

	database = data_dump.data_container()
	database.run_query('SELECT * FROM players_list')
	database.close_connection()
  
### Data Description
The data spans the NBA seasons from 2013-current and has 50747 records as of today.  There are 377 players and have stats for each player in each game they were part of and also other information like their college, hometown, birthdate, ect.

### Discussion
We also want team-by-team information (maybe?) if we want to compare a player against the average stats of the opponent but we can roll up all of the players stats on the opposing team.  Additionally, we might want to collect team information to check the accuracy of our own data.

There are other advanced statistics on the nba-reference site that may be worth reproducing.


### Notes
In some cases players dont play but we should record the reason for that...was it due to injury, coach choice, benched, or other?  This is in the data, just need to add it.
