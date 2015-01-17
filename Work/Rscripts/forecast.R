library(forecast)
library(zoo)
library("TTR")
library(ggplot2)
require('hydroGOF')
# setwd('Dev/HonsProject/Work/Rscripts')

data <- read.zoo(file='Sochi.csv', sep = ",", header = TRUE, 
                 index = 1:1, tz = "", format = "%Y-%m-%d")
# rdaead.csv('../tidydata/joined/Sochi.csv')

#data <- data[complete.cases(data), ]

sochi_ts <- ts(data$Searches, frequency=7)
plot.ts(sochi_ts)
# sochi_smoothed <- ts(SMA(sochi_ts, n=6), frequency=7)[6:430]
# plot.ts(sochi_smoothed)

decomposed <- decompose(x=sochi_ts,type='additive')
plot(decomposed)
#acf(sochi_smoothed, lag.max=20)
#pacf(sochi_smoothed, lag.max=20)

# sochi_arima <- arima(x=sochi_smoothed, order=c(5,1,0))
sochi_arima <- auto.arima(sochi_ts[1:400])
sochi_forecasts <- forecast.Arima(sochi_arima, h=30)
plot.forecast(sochi_forecasts)
predicted_vals <- sochi_forecasts$mean
actual_vals <- sochi_ts[400:431]


# ar_model <- ar(sochi_ts[1:400])
# ar_model$order <- 28
# for (i in 1:28){
#   ar_model$ar[i:i]<-0
# }
# ar_model$ar[7:7] <- 0.675
# ar_model$ar[14:14] <- 0.225
# ar_model$ar[21:21] <- 0.075
# ar_model$ar[28:28] <- 0.025
# 
# ar_forecast <- forecast.ar(ar_model, h=30)
# plot.forecast(ar_forecast)

#plot(fitted(sochi_arima))
#plot(fitted(ar_model))

df <- data.frame(Predicted=NA, Actual=NA)

for(i in 30:430){
  sochi_arima <- auto.arima(sochi_ts[1:i])
  sochi_forecasts <- forecast.Arima(sochi_arima, h=1)
  predicted_vals <- sochi_forecasts$mean
  actual_vals <- sochi_ts[i:i+1]
  # writeLines(paste(predicted_vals, ' ', actual_vals))
  df <- rbind(df, c(predicted_vals, actual_vals))
}

df <- df[complete.cases(df), ]

writeLines('Cross validated scores:')
writeLines('1. ARIMA scores')
writeLines(paste("MAPE is: ",mean(abs((df$Actual - df$Predicted)/df$Actual))))
writeLines(paste("RMSE is: ", rmse(df$Actual, df$Predicted, na.rm=TRUE)))


df_l4f <- data.frame(Predicted=NA, Actual=NA)

for(i in 30:430){
  c1 <- i-7
  c2 <- i-14
  c3 <- i-21
  c4 <- i-28
  l4f_value <- 0.675*sochi_ts[c1:c1] + 0.225*sochi_ts[c2:c2] + 0.075*sochi_ts[c3:c3] + 0.025*sochi_ts[c4:c4]
  actual_vals <- sochi_ts[i:i+1]
  # writeLines(paste(predicted_vals, ' ', actual_vals))
  df_l4f <- rbind(df_l4f, c(l4f_value, actual_vals))
}

df_l4f <- df_l4f[complete.cases(df_l4f), ]
writeLines('2. Last 4 Fridays score:')
writeLines(paste("MAPE is: ",mean(abs((df_l4f$Actual - df_l4f$Predicted)/df_l4f$Actual))))
writeLines(paste("RMSE is: ", rmse(df_l4f$Actual, df_l4f$Predicted, na.rm=TRUE)))

library("changepoint")
set.seed(10)
m.data <- c(rnorm(100, 0, 1), rnorm(100, 1, 1), rnorm(100, 0, 1),
               + rnorm(100, 0.2, 1))
ts.plot(m.data, xlab = "Index")
m.pelt <- cpt.mean(m.data, method = "PELT")
plot(m.pelt, type = "l", cpt.col = "blue", xlab = "Index", cpt.width = 4)
cpts(m.pelt)



ts.plot(sochi_ts, xlab="index")
sochi_cpts <- cpt.mean(sochi_ts[1:430], method='PELT')
plot(sochi_cpts, type = "l", cpt.col = "blue", xlab = "Index", cpt.width = 4)
cpts(sochi_cpts)

sochi_cpts <- cpt.var(sochi_ts[1:430])
plot(sochi_cpts, type = "l", cpt.col = "blue", xlab = "Index", cpt.width = 4)
sochi_cpts <- cpt.mean(sochi_ts[1:430])
plot(sochi_cpts, type = "l", cpt.col = "blue", xlab = "Index", cpt.width = 4)

sochi_cpts <- cpt.mean(sochi_ts[1:430],method = "SegNeigh")
plot(sochi_cpts, type = "l", cpt.col = "blue", xlab = "Index", cpt.width = 4)

sochi_meanvar <- cpt.meanvar(sochi_ts[1:430], test.stat = "Poisson", method='SegNeigh')
plot(sochi_meanvar, cpt.width = 3)
lines(fitted(sochi_arima), col ='blue')
cpts.ts(sochi_meanvar)

logl <- 0
sochi_arima <- arima(x = place_ts[1:400]), order=c(4,1,5))
logl <- logl + sochi_arima$loglik
logl

last_one <- 0
loglik <- 0
for(i in cpts.ts(sochi_meanvar)){
#writeLines(paste('at ', i))
  arma <- arima(place_ts[last_one:i], order=c(4,1,5))
  loglik <- arma$loglik + loglik
  #writeLines(paste('Log likelihood is', arma$loglik))
  #plot(fitted(arma), col='blue')
  #lines(place_ts[last_one:i])
  last_one <- i
}
writeLines(paste("Log likelihood from piecewise fit is ", loglik))

sochi_meanvar <- cpt.meanvar(sochi_ts[1:400], test.stat = "Poisson", method='SegNeigh')
plot(sochi_meanvar, cpt.width = 3)
lines(fitted(sochi_arima), col='blue')

sochi_meanvar <- cpt.meanvar(sochi_ts[1:430], test.stat = "Normal", method='SegNeigh')
plot(sochi_meanvar, cpt.width = 3)

sochi_meanvar <- cpt.meanvar(sochi_ts[1:430], test.stat = "Gamma", method='SegNeigh')
plot(sochi_meanvar, cpt.width = 3)

sochi_meanvar <- cpt.meanvar(sochi_ts[1:430], test.stat = "Exponential", method='SegNeigh')
plot(sochi_meanvar, cpt.width = 3)





# duration <- rpois(500, 10) # For duration data I assume Poisson distributed
# hist(duration,
#      probability = TRUE, # In stead of frequency
#      breaks = "FD",      # For more breaks than the default
#      col = "darkslategray4", border = "seashell3")
# lines(density(duration - 0.5), col = "firebrick2", lwd = 3)

hist(sochi_ts, probability = TRUE, breaks = 'FD', col = "darkslategray4", border = "seashell3")
lines(density(sochi_ts[1:430]), col='firebrick2', lwd = 3)





