library(ggplot2)

#RMSE Scatter

data <- read.csv('../results/results.csv')

max.val = max(data$RMSE_Twitter)
nx = seq(1, max.val-1, by=max.val/874)
ny = seq(1, max.val-1, by=max.val/874)

ggplot(data=data, aes(x=RMSE_Twitter, y=RMSE_L4F)) +
  geom_point(colour="#9932CC", size=1) + 
  #geom_smooth(method=lm) + 
  geom_line(aes(x=nx, y = ny), colour = '#00BFFF', size=0.5) + 
  scale_x_log10()  +
  xlab("Root mean squared error from the Twitter regression") + 
  scale_y_log10() +
  ylab("Root mean squared error from the L4F regression") + 
  ggtitle("RMSE scatter plot of classifiers") + 
  guides(fill = guide_legend(reverse=FALSE))

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