

###################################################################################
# metrics list
# mae, mse, 




mae=function(predict,actual){
  error=abs(predict-actual)
  error=sum(error)
  return(error)
}

mse=function(predict,actual){
  error=(predict-actual)^2
  error=sum(error)
  return(error)
}

print_metrics=function(predict,actual){
  
  mae_actual=mae(predict,actual)
  mse_actual=mse(predict,actual)
  
  mse_vec=c()
  mae_vec=c()
  
  for(i in 1:100){
    shuffled=sample(predict)
    mae_temp=mae(shuffled,actual)
    mse_temp=mse(shuffled,actual)
    
    mae_vec=c(mae_vec,mae_temp)
    mse_vec=c(mse_vec,mse_temp)
  }
  
  txt=paste('Error for mae is:',mae_actual,sep=' ')
  print(txt)
  
  txt=paste('Average error for mae is:',mean(mae_vec),sep=' ')
  print(txt)
  
  txt=paste('Percentile for mae is:',sum(mae_actual>mae_vec)/100,sep=' ')
  print(txt)
  
  
  txt=paste('Error for mse is:',mse_actual,sep=' ')
  print(txt)
  
  txt=paste('Average error for mse is:',mean(mse_vec),sep=' ')
  print(txt)
  
  txt=paste('Percentile for mse is:',sum(mse_actual>mse_vec)/100,sep=' ')
  print(txt)
  
}


