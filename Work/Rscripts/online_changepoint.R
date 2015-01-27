library(ggplot2)
library(forecast)
library(zoo)
library("TTR")
library('hydroGOF')
library('changepoint')
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

for(i in 30:430){
  arima <- arima(place_ts[1:i], order=c(4,1,5), method='ML')
  forecast <- forecast.Arima(arima, h=1)
  predicted_vals <- forecast$mean
  actual_vals <- place_ts[i:i+1]
  error <- predicted_vals - actual_vals
  writeLines(paste(i, " ", error))
  changepoint <- 0
  
  
  if(i > 35){
    df_arima <- df_arima[complete.cases(df_arima), ]
    num <- i - 30
    writeLines(paste("WE have x lines" , num))
    dt <- data.frame(x=c(1:num),y=df_arima$Error)
    dens <- density(dt$y)
    df <- data.frame(x=dens$x, y=dens$y)
    probs <- c(0.97, 0.98, 0.99)
    quantiles <- quantile(dt$y, prob=probs)
    df$quant <- factor(findInterval(df$x,quantiles))
    ggplot(df, aes(x,y)) + geom_line() + geom_ribbon(aes(ymin=0, ymax=y, fill=quant)) + scale_x_continuous(breaks=quantiles) + scale_fill_brewer(guide="none")
    
    
    parition <- 4 - as.integer(i/133)
    writeLines(paste("The quanttile we're looking at is ", quantiles[partition]))
    if (error > quantiles[partition]){
      writeLines('CHANGEPOINT')
      changepoint <- 1
    }
  }
  
  df_arima <- rbind(df_arima, c(predicted_vals, actual_vals, error, changepoint))
}

df_arima <- df_arima[complete.cases(df_arima), ]
# plot them all and find the quantiles