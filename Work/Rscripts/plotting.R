library(ggplot2)
library(reshape)
library(scales)

setwd('Dev/HonsProject/Work/Rscripts')


dfalpharmse <- read.csv('../results/alpha-rmse.csv')
dfalpharmse <- melt(dfalpharmse, id.vars=c('Place', 'Alpha'))

dfplot <- subset(dfalpharmse, dfalpharmse$Place=='united kingdom')
dfplot <- rbind(dfplot, subset(dfalpharmse, dfalpharmse$Place=='sochi'))
dfplot <- rbind(dfplot, subset(dfalpharmse, dfalpharmse$Place=='London'))
dfplot <- rbind(dfplot, subset(dfalpharmse, dfalpharmse$Place=='ukraine'))
#dfplot <- rbind(dfplot, subset(dfalpharmse, dfalpharmse$Place=='united kingdom'))

#

ggplot(data=dfplot, aes(x=Alpha, y=value, group=variable, colour=variable)) +
  geom_line(size=1.25) + facet_wrap( ~ Place,  scales="free") + 
  #geom_line(aes(x=nx, y=ny), size=1, colour="#4B0082")+ 
  scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) +
  scale_y_log10() + #scale_x_log10() +
  xlab("Alpha penalisation factor") + 
  ylab("RMSE") + 
  ggtitle("Reductions of RMSE with increase in penalisation parameter")

################################################################################


#RMSE Scatter
data <- read.csv('../results/lasso-static-and-dynamic.csv')

data <- data[complete.cases(data), ]
data <- do.call(data,lapply(data, function(x) replace(x, is.infinite(x),NA)))

data$RMSE.TwitterDF <- as.numeric(data$RMSE.TwitterDF)
data$RMSE.TwitterCF <- as.numeric(data$RMSE.TwitterCF)
data$RMSE_L4F <- as.numeric(data$RMSE_L4F)

max.val <- max(data$RMSE.TwitterCF)
nx = seq(1, max.val-1, by=max.val/1367)
ny = seq(1, max.val-1, by=max.val/1367)

ggplot(data=data, aes(x=RMSE_L4F, y=RMSE.TwitterDF)) +
  geom_point(size=2, colour = "#EE82EE") + 
  geom_line(aes(x=nx, y=ny), size=1, colour="#4B0082")+ 
  #scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) +
  scale_x_log10() + scale_y_log10() +
  xlab("Root mean squared error from the L4F") + 
  ylab("Root mean squared error from TwitterDF") + 
  ggtitle("RMSE scatter plot of classifiers")
#stat_smooth(method='lm')

keeps <- c( "RMSE.TwitterDF", "RMSE_L4F", "RMSE.TwitterCF")
data <- data[(names(data) %in% keeps)]

data <- melt(data, id.vars=c("RMSE_L4F"))


ggplot(data=data, aes(x=RMSE_L4F, y=value, group=variable, colour=variable)) +
  geom_point(size=3) + facet_grid(variable ~ .) +
  #geom_line(aes(x=nx, y=ny), colour="#4B0082")+ 
  scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) + 
  xlab("Root mean squared error from the L4F regression") + 
  ylab("Root mean squared error from the Twitter regressions") + 
  ggtitle("RMSE scatter plot of classifiers") +
  stat_smooth(method='lm')

########################################################################################
# STDEV/RMSE PLOT

stdevdata <- read.csv('../results/stdevscatter2.csv')

drops <- c("Place", "RMSE.TwitterDF", "RMSE.TwitterCF", "RMSE_L4F")
stdevdata <- stdevdata[,!(names(stdevdata) %in% drops)]

stdevdata$CFImprove <- as.numeric(stdevdata$CFImprove)
stdevdata$DFImprove <- as.numeric(stdevdata$DFImprove)
stdevdata <- stdevdata[complete.cases(stdevdata), ]
#stdevdata <- do.call(stdevdata,lapply(stdevdata, function(x) replace(x, is.infinite(x),NA)))

stdevdata <- melt(stdevdata, id.vars=c("StDev"))


ggplot(data=stdevdata, aes(x=StDev, y=value, group=variable, colour=variable)) +
  geom_point(aes(size=StDev)) + facet_grid(variable ~ .) +
  scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) + 
  #scale_x_log10() + #scale_y_log10() +
  scale_y_continuous(limits=c(-0.8,0.8),labels = percent) +
  xlab("Standard deviation of searches divided by the mean") + 
  ylab("Percentage improvement") + 
  ggtitle("RMSE of models versus normlalised STDEV of searches ") + 
  stat_smooth(method='loess')


#############################################################################################
# Improvement against L4F

stdevdata <- read.csv('../results/stdevscatter2.csv')

drops <- c("Place", "RMSE.TwitterDF", "RMSE.TwitterCF", 'StDev', 'CFImprove')
stdevdata <- stdevdata[,!(names(stdevdata) %in% drops)]

stdevdata$CFImprove <- as.numeric(stdevdata$CFImprove)
stdevdata$DFImprove <- as.numeric(stdevdata$DFImprove)
stdevdata <- stdevdata[complete.cases(stdevdata), ]
#stdevdata <- do.call(stdevdata,lapply(stdevdata, function(x) replace(x, is.infinite(x),NA)))

stdevdata <- melt(stdevdata, id.vars=c("RMSE_L4F"))


ggplot(data=stdevdata, aes(x=RMSE_L4F, y=value, group=variable, colour=variable)) +
  geom_point(size=1.5) + facet_grid(variable ~ .) +
  scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) + 
  scale_x_log10() + #scale_y_log10() +
  scale_y_continuous(limits=c(-0.8,0.8),labels = percent) +
  xlab("RMSE L4F") + 
  ylab("Percentage improvement") + 
  ggtitle("Improvement in RMSE in TwitterDF against L4F RMSE.") +
  stat_smooth(method='loess')


#   theme(axis.text.x=element_blank(),
#         axis.text.y=element_blank(),
#         axis.ticks=element_blank()
#   )


################################################################################################
# OVERALL

data <- read.csv('../tidydata/joined/OVERALL.csv')
data$Date <- as.Date(data$Date,format="%d%/%m/%Y") #-%m-%d")
data <- data[complete.cases(data), ]

ggplot(data=data, aes(x=Date, y=NSearches)) + 
  #geom_line(aes(x=Date,y=Count), colour = '#FF6347', size=1)+
  geom_line(colour = '#4B0082', size=1) +
  xlab("Month") + ylab("Normalised searches") + 
  ggtitle("Plot of all searches over time") 
# +  scale_x_date(labels = date_format("%m-%Y"))

################################################################################################
# Destination

city <- 'Lugansk'
file <- paste('../tidydata/joined/', city, sep='')
file <- paste(file, '.csv',sep='')
data <- read.csv(file)

keeps <- c( "RMCount", "Date", "RMSearches")
data <- data[(names(data) %in% keeps)]
data <- data[complete.cases(data), ]
data$Date <- as.Date(data$Date,format="%Y-%m-%d")



df <- melt(data, id.vars=c("Date"))

ggplot(data=df, aes(x=Date, y=value, colour = varible, group=variable))+
  geom_line(colour = '#00BFFF', size=1) + facet_grid(variable ~ ., scales="free") +
  scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) + 
  ggtitle(paste(paste("Plot of ", city, sep=''), " tweets and searches over time", sep=''))+
  ylab("Searches and Tweets") + 
  xlab(paste('Normalised searches to and tweets about ', city, sep='')) +
  theme(axis.text.x=element_text(size=15))
  #  scale_x_date(labels = date_format("%m-%Y"))


################################################################################################
# Loads of destinations

destinations = c('Prague','Lisbon','Morocco','Los Angeles','Dubai','Tenerife',
                 'Austria','Singapore','Tokyo','Sweden','South Korea','Mexico',
                 'Hungary','Hong Kong','Palma','Vietnam','Manchester','Budapest',
                 'Alicante','Frankfurt','Norway','Croatia','Belgium','Kuala Lumpur','New Zealand',
                 'Phuket','Seoul','Denmark','Brussels','Cyprus','Vienna','Venice','Miami',
                 'Stockholm','St Petersburg','Copenhagen','Spain','United States','United Kingdom',
                 'Italy','London','Russia','Germany','France','Thailand','Turkey',
                 'Greece','New York','Australia','Bangkok','Paris','Barcelona','Portugal',
                 'India','Netherlands','Istanbul','Rome','Brazil','China','Amsterdam',
                 'Munich','Moscow','Indonesia','Japan','Milan','Canada','Ireland',
                 'Madrid','Sochi','Poland','Berlin','Switzerland','Dublin','Czech Republic',
                 'United Arab Emirates','Malaga','Philippines','Athens','Malaysia')

for (i in destinations){
  i='Tenerife'
  file = paste('../tidydata/predictions/', i, sep='')
  file = paste(file, '.csv',sep='')
  
  max.val <- max(df)
  nx <- seq(1, max.val-1, by=max.val/175)
  ny <- seq(1, max.val-1, by=max.val/175)
  
  df <- read.csv(file)
  df <- melt(df, id.vars=c("Actual"))
  
  ggobj = ggplot(data=df, aes(x=Actual, y=value, group=variable, colour=variable)) +
    geom_point(size=3) + facet_grid(. ~ variable) +
    scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) + 
    geom_abline(aes(colour=variable)) + 
    xlab("True searches") + ylab("Predicted searches") + 
    ggtitle("Scatter plot of all the different predictions against the actual values") +
    #stat_smooth(formula = y ~ x, method='lm') +
    theme(axis.line=element_blank(),
          axis.text.x=element_blank(),
          axis.text.y=element_blank(),
          axis.ticks=element_blank()
    )
  
  print(ggobj)
  ggsave(sprintf("../../write-up/plots/%s.pdf", i))
}

# SCATTER COUNT / SEARCHES


city <- 'London'
file <- paste(city, '.csv',sep='')
file <- paste('../tidydata/joined/', file, sep='')
title <- paste("Scatter of searches against Twitter counts for ", city, sep='')

df_scatter <- read.csv(file)

keeps <- c( "Unnamed..0.1")
df_scatter <- df_scatter[!(names(df_scatter) %in% keeps)]
df_scatter <- df_scatter[complete.cases(df_scatter), ]

ggplot(data=df_scatter, aes(x=Count, y=NSearches)) +
  geom_point(size=3, colour = "#4B0082") +
  xlab("Twitter counts") + 
  ylab("Searches") + 
  scale_x_log10() +
  ggtitle(title) + stat_smooth(method='loess', colour="#FF6347")

# df_scatter <- read.csv('../tidydata/1dayshift/Dublin.csv')
# 
# keeps <- c( "Unnamed..0.1")
# df_scatter <- df_scatter[!(names(df_scatter) %in% keeps)]
# df_scatter <- df_scatter[complete.cases(df_scatter), ]
# 
# ggplot(data=df_scatter, aes(x=Count, y=NSearches)) +
#   geom_point(size=3, colour = "#4B0082") +
#   xlab("Twitter counts") + 
#   ylab("Searches") + 
#   ggtitle("Searches against Twitter counts for London") +
#   stat_smooth(method='loess', colour="#FF6347")

###############################################################################################
# Hashtag and counts

handc <- read.csv('../tidydata/London-all.csv')
handc <- handc[complete.cases(handc), ]
handc$Date <- as.Date(handc$Date,format="%Y-%m-%d")

handc <- melt(handc, id.vars=c("Date"))

ggplot(data=handc, aes(x=Date, y=value, group=variable, colour=variable)) +
  geom_line(size=1.2) + facet_grid(variable~.,scales='free') +
  scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) + 
  xlab("Number of hashtags/twitter counts") + ylab("Time") + 
  ggtitle("Twitter counts and hashtag counts") +
  stat_smooth(method='loess') +
  theme(axis.text.x=element_text(size=15))

###############################################################################################
# Reduction in RMSE and weights with alpha

wrmse <- read.csv('../results/weight-rmse.csv')
wrmse$Alpha <- as.factor(wrmse$Alpha) 

wrmse <- melt(wrmse, idf.vars=c('Alpha'))

ggplot(data=wrmse, aes(x=Alpha, y=value, group=variable, colour=variable)) +
  geom_line(size=1.2) + facet_wrap(~variable, ncol=2, scales='free') +
  scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) + 
  xlab("Value of alpha") + ylab("") + 
  ggtitle("Twitter counts and hashtag counts") +
  stat_smooth(method='loess') +
  theme(axis.text.x = element_text(angle = 45, size=10, hjust = 1))


############################################################################
# Scatter plot of FP vs Recall
############################################################################

data <- read.csv('FP_Recall_data.csv')

ggplot(data=data, aes(x=FP, y=Recall)) + 
  geom_point(size=3, colour='blue') + xlab("False Positives") + ylab("Recall") + 
  ggtitle("Plot of False positives against Recall")+
  stat_smooth(method='lm') + 
  theme(axis.text.x = element_text(angle = 45, size=10, hjust = 1))