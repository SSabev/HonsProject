library(ggplot2)
library(forecast)
library(zoo)
library("TTR")
library('hydroGOF')
library('changepoint')
library('reshape')
library('vars')
setwd('Dev/HonsProject/Work/Rscripts')

# Get all the errors
i <- 'FictionTown6'
place <- i
file <- paste(i,".csv", sep="")
data <- read.zoo(file=file, sep = ",", header = TRUE, 
                 index = 1:1, tz = "", format = "%Y-%m-%d")
place_ts <- ts(data)
plot.ts(place_ts)
df_arima <- data.frame(Predicted=NA, Actual=NA, Error=NA, ChangePoint=NA)
coef <- data.frame()


n <- 0
mean <- 0
M2 <- 0
numstdevs <- 4
changepoint_decay <-5 
found <- FALSE

for(i in 30:800){
  arima <- arima(place_ts[1:i], order=c(4,1,5), method='ML')
  #writeLines(paste("The coeff are ", arima$coef))
  forecast <- forecast.Arima(arima, h=1)
  predicted_vals <- forecast$mean
  actual_vals <- place_ts[i:i+1]
  error <- as.integer(predicted_vals - actual_vals)
  writeLines(paste(i, " ", error))
  changepoint <- 0
  
  n <- n + 1
  delta <- error - mean
  mean <- mean + delta/n
  M2 <- M2 + delta*(error - mean)
  variance <- M2/(n - 1)
  stdev <- sqrt(variance)
  
  if(i > 250){
    numstdevs <- 3
  }
  

  if(i > 35){
    df_arima <- df_arima[complete.cases(df_arima), ]
    num <- i - 30
    writeLines(paste("Online mean is ", mean, " and online stdev is ", stdev))

    if (error > mean + numstdevs*stdev || error < mean - numstdevs*stdev || !found){
      writeLines('CHANGEPOINT')
      changepoint <- 1
      found <- TRUE
    }
    
  }
  coef <- rbind(coef, arima$coef)
  df_arima <- rbind(df_arima, c(predicted_vals, actual_vals, error, changepoint))
}

df_arima <- df_arima[complete.cases(df_arima), ]
write.csv(df_arima, paste('Results/', place, '-result.csv', sep=''))
# plot them all and find the quantiles