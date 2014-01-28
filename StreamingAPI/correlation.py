import pandas as p
from scipy.stats import pearsonr, linregress
import glob
import matplotlib.pyplot as plt
import pylab

city = 'Paris'
searches_and_tweets = p.read_csv('tidydata/joined/%s.csv'%city)

plt.scatter(searches_and_tweets['Count'], searches_and_tweets['NSearches'])
plt.title('Scatter of twitter counts against searches for %s'%city)
r_value, p_value = pearsonr(searches_and_tweets['Count'], searches_and_tweets['NSearches'])
plt.xlabel(r"Twitter counts", fontsize = 12)
plt.ylabel(r"Search count (Normalised)", fontsize = 12)
pylab.show()

print (r_value, p_value)
