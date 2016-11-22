
require(data.table)


###################################################################################
# read data 


dir='c:\\Users\\James\\Desktop\\fanduel_project\\'
setwd(dir)

filename='parsed_data_2016-11-19.csv'

dataset=fread(filename)

# keep only people that played
table(dataset$reason_code)
dataset=dataset[reason_code=='complete']

# maybe we need to filter these..about 1/3 of data.
sum(dataset$total_fd_pts==0)

# remove early na
dataset=dataset[!is.na(pts_roll_six)]

# add a random variable
n=dim(dataset)[1]
dataset[,random_variable1:=sample(1:n)]
dataset[,random_variable2:=sample(1:n)]


# split data
test=dataset[date_game>='2015-01-01' & date_game<='2015-08-01']
train=dataset[date_game<'2015-01-01']



###################################################################################
# run model

# model comparisons
# 1. average model - use only past average total points
# 2. gbm model - use
# 3. linear model - trend-based model
# 4. arima model - time-series model


require(caret)

formula=total_fd_pts~pts_roll_three+
  stl_roll_three+
  blk_roll_three+
  tov_roll_three+
  trb_roll_three+
  tov_roll_three+
  
  pts_roll_six+
  stl_roll_six+
  blk_roll_six+
  tov_roll_six+
  trb_roll_six+
  tov_roll_six+
  
  random_variable1+
  random_variable2


formula=total_fd_pts~pts_roll_three+
  trb_roll_three+
  
  pts_roll_six+
  stl_roll_six+
  blk_roll_six+
  tov_roll_six+
  trb_roll_six+
  tov_roll_six+
  
  location
  
  
set.seed(1)

fitControl <- trainControl(
  method = "repeatedcv",
  number = 2,
  repeats = 2
)

gbmGrid <-  expand.grid(interaction.depth = c(10),
                        n.trees = c(500), 
                        shrinkage = c(0.01),
                        n.minobsinnode = c(20)
)

nrow(gbmGrid)

gbmFit1 <- train(formula, 
                 data = train, 
                 method = "gbm", 
                 trControl = fitControl,
                 verbose = T,
                 tuneGrid=gbmGrid
)

gbmFit1

ggplot(gbmFit1)  

summary(gbmFit1)  

# var    rel.inf
# pts_roll_six         pts_roll_six 62.7516138
# trb_roll_six         trb_roll_six  9.7898194
# pts_roll_three     pts_roll_three  9.5340452
# trb_roll_three     trb_roll_three  4.6372225
# tov_roll_six         tov_roll_six  3.0446749
# blk_roll_six         blk_roll_six  2.3715134
# stl_roll_six         stl_roll_six  2.0460697
# random_variable1 random_variable1  1.5992214
# random_variable2 random_variable2  1.5750297
# tov_roll_three     tov_roll_three  1.4037743
# blk_roll_three     blk_roll_three  0.7466272
# stl_roll_three     stl_roll_three  0.5003884




###################################################################################
# validation

source('data_transformation/Utility_metrics.R')
# Model error
model=gbmFit1
predictions=predict(model,newdata=test,n.trees=500)
# Model error
print_metrics(predictions,test$total_fd_pts)


# avg error
predictions=1.0*test$pts_roll_three+
  1.2**test$trb_roll_three+
  1.5**test$ast_roll_three+
  2.0**test$stl_roll_three+
  2.0**test$blk_roll_three+
  -1.0**test$tov_roll_three
print_metrics(predictions,test$total_fd_pts)


predictions=1.0*test$pts_roll_six+
  1.2**test$trb_roll_six+
  1.5**test$ast_roll_six+
  2.0**test$stl_roll_six+
  2.0**test$blk_roll_six+
  -1.0**test$tov_roll_six
print_metrics(predictions,test$total_fd_pts)


# Model improvement
31.7/34.5


# residuals
hist(test$total_fd_pts-predictions,breaks=100)
