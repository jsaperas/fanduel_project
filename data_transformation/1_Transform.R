

require(data.table)

###################################################################################
# read data 

dir='c:\\Users\\James\\Desktop\\fanduel_project\\data_pull_scripts/'
setwd(dir)


filename='sample.csv'
dataset=fread(filename)


###################################################################################
# data cleaning

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

require(zoo)

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
dataset[,trb_roll_three:=shifter(trb,k=6),by=(player_name)]
dataset[,ast_roll_three:=shifter(ast,k=6),by=(player_name)]
dataset[,tov_roll_three:=shifter(tov,k=6),by=(player_name)]
dataset[,blk_roll_three:=shifter(blk,k=6),by=(player_name)]
dataset[,stl_roll_three:=shifter(stl,k=6),by=(player_name)]


# create response
dataset[,total_fd_pts:=1.0*pts+
                       1.2*trb+
                       1.5*ast+
                       2.0*stl+
                       2.0*blk+
                      -1.0*tov
]


###################################################################################
# check data

dataset[player_name=='Solomon Hill']






###################################################################################
# write data

dir='c:\\Users\\James\\Desktop\\fanduel_project\\data_pull_scripts\\'

current_date=Sys.Date()
filename=paste('parsed_data_',current_date,'.csv',sep='')
filename=paste(dir,filename,sep='')

write.csv(dataset,
          file=filename,
          row.names=F)


