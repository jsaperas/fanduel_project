
# Transform data so we can model on it

require(data.table)





###################################################################################
# read data 

dir='c:\\Users\\James\\Desktop\\fanduel_project\\'
setwd(dir)


filename='data_pull_scripts\\sample.csv'
dataset=fread(filename)


###################################################################################
# data cleaning

# keep only complete
dataset=dataset[reason_code=='complete']

# remove strange values.
dataset=dataset[pts!='PTS']

# order
dataset=dataset[order(date_game,descending=T)]

# fix data types
dataset$pts=dataset$pts=ifelse(dataset$pts=='','0',dataset$pts)
dataset$pts=as.numeric(dataset$pts)

dataset$trb=dataset$trb=ifelse(dataset$trb=='','0',dataset$trb)
dataset$trb=as.numeric(dataset$trb)

dataset$blk=dataset$blk=ifelse(dataset$blk=='','0',dataset$blk)
dataset$blk=as.numeric(dataset$blk)

dataset$ast=dataset$ast=ifelse(dataset$ast=='','0',dataset$ast)
dataset$ast=as.numeric(dataset$ast)

dataset$tov=dataset$tov=ifelse(dataset$tov=='','0',dataset$tov)
dataset$tov=as.numeric(dataset$tov)

dataset$stl=dataset$stl=ifelse(dataset$stl=='','0',dataset$stl)
dataset$stl=as.numeric(dataset$stl)



###################################################################################
# feature creation

source('data_transformation\\Utility_functions.R')

# group by teams
teams=unique(dataset$opp_id)

team_defense=dataset[,.(pts_allowed=sum(pts),
                        reb_allowed=sum(trb)),
                        by=.(opp_id,date_game)]

dataset[date_game=='2012-10-30' & opp_id=='LAL']

position_defense=dataset[,.(pts_roll_six=shifter(opp_id,k=6)),by=.(opp_id,date_game,pos)]





###################################################################################
# check data

dataset[player_name=='Solomon Hill']






###################################################################################
# write data

dir='c:\\Users\\James\\Desktop\\fanduel_project\\data_pull_scripts\\'

current_date=Sys.Date()
filename=paste('opponent_data_',current_date,'.csv',sep='')
filename=paste(dir,filename,sep='')

write.csv(dataset,
          file=filename,
          row.names=F)




