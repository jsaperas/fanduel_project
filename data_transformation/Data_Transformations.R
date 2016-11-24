require(data.table)
filename='../data_pull_scripts/sample.csv'
dataset=fread(filename)

source('Utility_functions.R')

# remove strange values.

dataset=dataset[reason_code=='complete']
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

#Aggregate metrics allowed by opponent team by game by positions
defense = dataset[,.(pts_allowed=sum(pts),
                        reb_allowed=sum(trb),
                        ast_allowed=sum(ast),
                        tov_allowed=sum(tov),
                        blk_allowed=sum(blk),
                        stl_allowed=sum(stl)
          ),
                        by=.(opp_id,date_game,pos)]

#Calculate 3 game moving average for allowed metrics
defense[,pts_allowed_3:=shifter(pts_allowed,k=3),by=.(opp_id,pos)]
defense[,reb_allowed_3:=shifter(reb_allowed,k=3),by=.(opp_id,pos)]
defense[,ast_allowed_3:=shifter(ast_allowed,k=3),by=.(opp_id,pos)]
defense[,tov_allowed_3:=shifter(tov_allowed,k=3),by=.(opp_id,pos)]
defense[,blk_allowed_3:=shifter(blk_allowed,k=3),by=.(opp_id,pos)]
defense[,stl_allowed_3:=shifter(stl_allowed,k=3),by=.(opp_id,pos)]

#Drop raw points only keep game moving averages
defense = defense[,.(opp_id,date_game,pos,pts_allowed_3,reb_allowed_3,ast_allowed_3,tov_allowed_3,blk_allowed_3,stl_allowed_3)]

#Join defense points allowed with dataset
library(plyr)
dataset = join(dataset, defense, by=c('opp_id','date_game','pos'))

###################################################################################
#Additional transformations

# Home vs away
dataset$home=dataset$home=ifelse(dataset$location=='',1,0)

# Win inidcator
dataset$win =ifelse(substr(dataset$game_result, 1, 1) =='W',1,0)

#Age cleaned
dataset$age_cleaned =as.numeric(substr(dataset$age, 1, 2))

#Minutes played in decimal and 3 game average
dataset$minutes_played= as.numeric(gsub(":.*","",dataset$mp)) + round(as.numeric(gsub(".*:","",dataset$mp))/60,2)
dataset[,minutes_played_3:=shifter(minutes_played,k=3),by=.(player_name)]


#Days in between games --- Not working correctly yet

days_between=function(x){
  x = as.Date(strptime(x, "%m/%d/%Y"))  
  n=length(x)
  if (n>=2){
      days=as.numeric(x[2:n] - x[1:(n-1)])
  }else{
      return(NA)
  }
    vec=c(NA,days)
    return(vec)
}

dataset[,rest_days:=days_between(date_game),by=.(team_id)]