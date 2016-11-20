
require(data.table)


###################################################################################
# read data 

dir='c:\\Users\\James\\Desktop\\fanduel_project\\data_pull_scripts/'
setwd(dir)

filename='parsed_data_2016-11-19.csv'

dataset=fread(filename)

# maybe we need to filter these..about 1/3 of data.
sum(dataset$total_fd_pts==0)


dataset=dataset[!is.na(pts_roll_three)]

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
  tov_roll_three

set.seed(1)

fitControl <- trainControl(
  method = "repeatedcv",
  number = 3,
  repeats = 2
)

gbmGrid <-  expand.grid(interaction.depth = c(2, 10), 
                        n.trees = c(250,500), 
                        shrinkage = c(0.01),
                        n.minobsinnode = c(10)
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






###################################################################################
# validation

model=gbmFit1
predictions=predict(model,newdata=test,n.trees=500)



# print error
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



# Model improvement
31.7/34.5


# residuals
hist(test$total_fd_pts-predictions,breaks=100)
