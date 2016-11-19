

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



# create features
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
dataset[,trb_roll_three:=shifter(pts,k=6),by=(player_name)]
dataset[,ast_roll_three:=shifter(pts,k=6),by=(player_name)]
dataset[,tov_roll_three:=shifter(pts,k=6),by=(player_name)]
dataset[,blk_roll_three:=shifter(pts,k=6),by=(player_name)]
dataset[,stl_roll_three:=shifter(pts,k=6),by=(player_name)]


# response
dataset[,total_fd_pts:=1.0*pts+
                       1.2*trb+
                       1.5*ast+
                       2.0*stl+
                       2.0*blk+
                      -1.0*tov
]


#dataset[,three_mean:=rollapplyr(as.numeric(pts),list(-(min(NROW(pts),6):1)),mean,fill=NA),by=(player_name)]

dataset[player_name=='Solomon Hill']







# All games
# split data to train / test
train=dataset[date_game<'2015-01-01']
test=dataset[date_game>='2015-01-01' & date_game<'2015-08-01']
