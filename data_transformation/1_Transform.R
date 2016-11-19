

require(data.table)

dir='c:\\Users\\James\\Desktop\\fanduel_project\\data_pull_scripts/'
setwd(dir)


filename='sample.csv'
dataset=fread(filename)


# remove strange values.
dataset=dataset[pts!='PTS']

# For all games, calculate rolling mean of all previous games.
require(zoo)

dataset=dataset[order(date_game,descending=T)]
dataset$pts=dataset$pts=ifelse(dataset$pts=='','0',dataset$pts)



shifter=function(x,k=6){
  n=length(x)
  x=rollmean(as.numeric(x),align='right',k=min(NROW(x),k),fill=NA)
  
  if(n==1){
    return(x)
  }else{
    vec=x[1:(n-1)]
    vec=c(NA,vec)
    return(vec)
  }
}
dataset[,pts_roll_three:=shifter(pts,k=6),by=(player_name)]
dataset[,three_mean:=shifter(pts),by=(player_name)]




#dataset[,three_mean:=rollapplyr(as.numeric(pts),list(-(min(NROW(pts),6):1)),mean,fill=NA),by=(player_name)]

dataset[player_name=='Solomon Hill']




# create response variable





# All games
# split data to train / test
train=dataset[date_game<'2015-01-01']
test=dataset[date_game>='2015-01-01' & date_game<'2015-08-01']
