library(ggplot2)


data <- read.csv('../results/results.csv')

max.val = max(data$RMSE_Twitter)
nx = seq(1, max.val-1, by=max.val/468)
ny = seq(1, max.val-1, by=max.val/468)

ggplot(data=data, aes(x=RMSE_Twitter, y=RMSE_L4F)) +
  geom_point(fill ='blue', size=1) + 
  #geom_smooth(method=lm) + 
  geom_line(aes(x=nx, y = ny), colour = 'blue', size=0.5) + 
  scale_x_log10()  +
  xlab("Root mean squared error from the Twitter regression") + 
  scale_y_log10() +
  ylab("Root mean squared error from the L4F regression") + 
  ggtitle("RMSE scatter plot of classifiers") + 
  guides(fill = guide_legend(reverse=FALSE))
