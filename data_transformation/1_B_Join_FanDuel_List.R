require(data.table)

#Read in list of players for this week (night, contest, ...) 
filename='FanDuel-NBA-2016-12-01-17147-players-list.csv'
player_list=fread(filename)

#Read in player_data and defense data
dir='../data/'

filename1=paste(dir,'player_data_example.csv', sep='')
filename2=paste(dir,'defense_data_example.csv',sep='')

player_data=fread(filename1)
defense_data =fread(filename2)

#Change column names to remove space
setnames(player_list,'First Name','First_Name')
setnames(player_list,'Last Name','Last_Name')
setnames(defense_data,'opp_id','Opponent')

#Add full name to player list
player_list[, player_name := paste(First_Name,Last_Name)]

#Grab the last (most recent) row of data for each player. 
library(plyr)
recent_player = ddply(player_data, .(player_name), function(x) x[nrow(x), ])
recent_defense = ddply(defense_data, .(Opponent), function(x) x[nrow(x), ])

#Join most recent player and oppinent team stats to player list
player_list = join(player_list, recent_player, by=c('player_name'))
player_list = join(player_list, recent_defense, by=c('Opponent'))


#Write data to file. Ready for predicting points
dir='../data/'

filename=paste('player_list_example.csv',sep='')
filename=paste(dir,filename,sep='')

write.csv(player_list,
          file=filename,
          row.names=F)