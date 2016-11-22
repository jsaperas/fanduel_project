

########################################################################################
# This section will store useful functions for transformations. Should we just create a library?



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

