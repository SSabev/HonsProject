library(ggplot2)
library(forecast)
library(zoo)
library("TTR")
library('hydroGOF')
library('changepoint')
library('reshape')
setwd('Dev/HonsProject/Work/Rscripts')

# Get all the errors
i <- 'Sochi'
place <- i
file <- paste(i,".csv", sep="")
data <- read.zoo(file=file, sep = ",", header = TRUE, 
                 index = 1:1, tz = "", format = "%Y-%m-%d")
place_ts <- ts(data$Searches)
plot.ts(place_ts)
df_arima <- data.frame(Predicted=NA, Actual=NA, Error=NA, ChangePoint=NA)

n <- 0
mean <- 0
M2 <- 0
numstdevs <- 4
changepoint_decay <-5 
found <- FALSE

arima <- auto.arima(place_ts[1:30], method='ML')

for(i in 30:153){
  num_forecasts <- i-29
  forecast <- forecast.Arima(arima, h=num_forecasts)
  predicted_vals <- forecast$mean[num_forecasts]
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
    dt <- data.frame(x=c(1:num),y=df_arima$Error)
    dens <- density(dt$y)
    df <- data.frame(x=dens$x, y=dens$y)
    writeLines(paste("Online mean is ", mean, " and online stdev is ", stdev))
    #     if(found && changepoint_decay > 1){
    #       changepoint_decay <- changepoint_decay - 1
    #     }
    #     
    #     if(changepoint_decay == 1){
    #       changepoint_decay <- 5
    #       found <- FALSE
    #     }
    #     
    if (error > mean + numstdevs*stdev || error < mean - numstdevs*stdev || !found){
      writeLines('CHANGEPOINT')
      changepoint <- 1
      found <- TRUE
      arima <- auto.arima(place_ts[1:i], method='ML')
    }
    
    
  }
  
  df_arima <- rbind(df_arima, c(predicted_vals, actual_vals, error, changepoint))
}

df_arima <- df_arima[complete.cases(df_arima), ]
# plot them all and find the quantiles