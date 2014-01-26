import pandas as p
from scipy.stats import pearsonr, linregress
import datetime as dt
from dateutil.relativedelta import relativedelta
import glob
import matplotlib.pyplot as plt

city = 'Dublin'
searches_and_tweets = p.read_csv('tidydata/joined/%s.csv'%city)

plt.scatter(searches_and_tweets['Count'], searches_and_tweets['NSearches'])
plt.title('Scatter of twitter counts against searches for %s'%city)
# gradient, intercept, r_value, p_value, std_err = linregress(searches_and_tweets['Count'], searches_and_tweets['Searches'])
plt.xlabel(r"Twitter counts", fontsize = 12)
plt.ylabel(r"Search count (Normalised)", fontsize = 12)
pylab.show()
