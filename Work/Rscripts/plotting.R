library(ggplot2)
library(reshape)
#RMSE Scatter

data <- read.csv('../results/lasso-static-and-dynamic.csv')

data <- data[complete.cases(data), ]
data <- do.call(data,lapply(data, function(x) replace(x, is.infinite(x),NA)))

data$RMSE.TwitterDF <- as.numeric(data$RMSE.TwitterDF)
data$RMSE.TwitterCF <- as.numeric(data$RMSE.TwitterCF)
data$RMSE_L4F <- as.numeric(data$RMSE_L4F)

max.val <- max(data$RMSE.TwitterCF)
nx = seq(1, max.val-1, by=max.val/982)
ny = seq(1, max.val-1, by=max.val/982)

keeps <- c("RMSE.TwitterCF", "RMSE.TwitterDF", "RMSE_L4F")
data <- data[(names(data) %in% keeps)]

data <- melt(data, id.vars=c("RMSE_L4F"))

ggplot(data=data, aes(x=RMSE_L4F, y=value, group=variable, colour=variable)) +
  geom_point(size=3) + facet_grid(. ~ variable) +
  scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) + 
  xlab("Root mean squared error from the L4F regression") + 
  ylab("Root mean squared error from the Twitter regressions") + 
  ggtitle("RMSE scatter plot of classifiers") +
  stat_smooth(method='lm')

# OVERALL

data <- read.csv('../tidydata/joined/OVERALL.csv')
data$Date <- as.Date(data$Date,format="%Y-%m-%d")

ggplot(data=data, aes(x=Date, y=NSearches)) + 
  geom_line(colour = '#00BFFF', size=1) +
  xlab("Month") + ylab("Normalised searches") + 
  ggtitle("Plot of all searches over time") 
# +  scale_x_date(labels = date_format("%m-%Y"))

# Destiaation

data <- read.csv('../tidydata/joined/Ibiza.csv')
data$Date <- as.Date(data$Date,format="%Y-%m-%d")

ggplot(data=data, aes(x=Date, y=NSearches)) + 
  geom_line(colour = '#00BFFF', size=1) +
  xlab("Month") + ylab("Normalised searches") + 
  ggtitle("Plot of searches to Ibiza over time") 
  # +  scale_x_date(labels = date_format("%m-%Y"))


destinations = c('alicante',  'amsterdam',  'athens',  'australia',  'austria',  'bangkok',  'barcelona',  'berlin',  'china',  'cuba',  'cyprus',  'dubai',  'dublin',  'faro',  'france',  'geneva',  'germany',  'greece',  'havana',  'ibiza',  'iceland',  'india',  'istanbul',  'italy',  'lanzarote',  'London',  'madrid',  'malaga',  'manchester',  'milan',  'morocco',  'Moscow',  'munich',  'netherlands',  'palma',  'paris',  'portugal',  'rome',  'russia',  'spain',  'switzerland',  'tenerife',  'thailand',  'thessaloniki',  'turkey',  'vietnam')

for (i in destinations){
  file = paste('../tidydata/predictions/', i, sep='')
  file = paste(file, '.csv',sep='')
  
  df <- read.csv(file)
  df <- melt(df, id.vars=c("Actual"))
  
  ggobj = ggplot(data=df, aes(x=Actual, y=value, group=variable, colour=variable)) +
    geom_point(size=3) + facet_grid(. ~ variable) +
    scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) + 
    xlab("True searches") + ylab("Predicted searches") + 
    ggtitle("Scatter plot of all the different predictions against the actual values") +
    stat_smooth(method='lm') +
    theme(axis.line=element_blank(),
          axis.text.x=element_blank(),
          axis.text.y=element_blank(),
          axis.ticks=element_blank()
    )
  
  print(ggobj)
  ggsave(sprintf("../../write-up/plots/%s.pdf", i))
}


  
  
