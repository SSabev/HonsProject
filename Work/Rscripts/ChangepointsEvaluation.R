library(forecast)
library(zoo)
library("TTR")
library(ggplot2)
library('hydroGOF')
library('changepoint')

#setwd('Dev/HonsProject/Work/Rscripts')

destinations = c('Brazil', 'Sochi', 'Fukuoka', 'Ukraine', 'Venezuela', 'Sevastopol', 
                 'North Korea', 'Uruguay')

results_df <- data.frame(Place=NA, L4F=NA, ARIMA=NA)

for (i in destinations){
  # i <- 'Sochi'
  place <- i
  file <- paste(i,".csv", sep="")
  data <- read.zoo(file=file, sep = ",", header = TRUE, 
                   index = 1:1, tz = "", format = "%Y-%m-%d")
  
  df_l4f <- data.frame(Predicted=NA, Actual=NA)
  place_ts <- ts(data$Searches)
  plot.ts(place_ts)
  for(i in 30:430){
    c1 <- i-7
    c2 <- i-14
    c3 <- i-21
    c4 <- i-28
    l4f_value <- 0.675*place_ts[c1:c1] + 0.225*place_ts[c2:c2] + 0.075*place_ts[c3:c3] + 0.025*place_ts[c4:c4]
    actual_vals <- place_ts[i:i+1]
    # writeLines(paste(predicted_vals, ' ', actual_vals))
    df_l4f <- rbind(df_l4f, c(l4f_value, actual_vals))
  }
  
  writeLines(paste("MAPE is: ",mean(abs((df_l4f$Actual - df_l4f$Predicted)/df_l4f$Actual))))
  writeLines(paste("RMSE is: ", rmse(df_l4f$Actual, df_l4f$Predicted, na.rm=TRUE)))
  
  
  df <- data.frame(Predicted=NA, Actual=NA)
  
  for(i in 30:430){
    arima <- arima(place_ts[1:i], order=c(4,1,5), method='ML')
    forecast <- forecast.Arima(arima, h=1)
    predicted_vals <- forecast$mean
    actual_vals <- place_ts[i:i+1]
    df <- rbind(df, c(predicted_vals, actual_vals))
  }
  
  df <- df[complete.cases(df), ]
  
  df$Error <- df$Actual - df$Predicted
  
  
  writeLines(paste("MAPE is: ",mean(abs((df$Actual - df$Predicted)/df$Actual))))
  writeLines(paste("RMSE is: ", rmse(df$Actual, df$Predicted, na.rm=TRUE)))
  
  dd <- density(df$Error)
  
  results_df <- rbind(results_df, c(place, rmse(df_l4f$Actual, df_l4f$Predicted, na.rm=TRUE), rmse(df$Actual, df$Predicted, na.rm=TRUE)))
  #   logl <- 0
  #   sochi_arima <- arima(x = place_ts[1:400]), order=c(4,1,5))
  #   logl <- logl + sochi_arima$loglik
  #   logl
  #   
  #   last_one <- 0
  #   loglik <- 0
  #   for(i in cpts.ts(sochi_meanvar)){
  #     #writeLines(paste('at ', i))
  #     arma <- arima(place_ts[last_one:i], order=c(4,1,5))
  #     loglik <- arma$loglik + loglik
  #     #writeLines(paste('Log likelihood is', arma$loglik))
  #     #plot(fitted(arma), col='blue')
  #     #lines(place_ts[last_one:i])
  #     last_one <- i
  #   }
}
results_df <- results_df[complete.cases(results_df), ]
results_df$L4F <- as.numeric(results_df$L4F)
results_df$ARIMA <- as.numeric(results_df$ARIMA)
wilcox.test(results_df$L4F, results_df$ARIMA, paired=TRUE)
