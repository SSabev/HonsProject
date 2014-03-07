library(ggplot2)
library(reshape)
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


df <- read.csv('../tidydata/predictions/london.csv')

#df$TwitterCF <- df$TwitterCF/max(df$TwitterCF)
#df$TwitterDF <- df$TwitterDF/max(df$TwitterDF)
#df$L4F <- df$L4F/max(df$L4F)
#df$Actual <- df$Actual/max(df$Actual)

df <- melt(df, id.vars=c("Actual"))

ggplot(data=df, aes(x=Actual, y=value, group=variable, colour=variable)) +
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
  
  
