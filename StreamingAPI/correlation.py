import pandas as p
import scipy
from scipy.stats import pearsonr, linregress
import matplotlib.pyplot as plt
import datetime as dt

city = 'London'

searches = p.read_csv('tidydata/se/%s.csv'%city)

def conversion(date):
    return dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

searches.Date = searches.Date.apply(conversion)
tweets = p.read_csv('tc/%s.csv'%city)

tweets['Date'] = tweets['Datetime']

searches_and_tweets = searches.merge(tweets, on='Date', how='inner')
del searches_and_tweets['KeyWord']

#r_row, p_value = pearsonr(earches_and_tweets['Count'], earches_and_tweets['Searches'])

searches_and_tweets['NSearches'] = searches_and_tweets['Searches']/float(max(searches_and_tweets['Searches']))
del searches_and_tweets['Searches']

plt.scatter(searches_and_tweets['Count'], searches_and_tweets['NSearches'])
plt.title('Scatter of twitter counts against searches for %s'%city)

plt.xlabel(r"Twitter counts", fontsize = 12)
plt.ylabel(r"Search count (Normalised)", fontsize = 12)
plt.show()


# For london bigger dataset
# In [39]: r_row, p_value
# Out[39]: (0.13016098564086925, 0.28283460745375955)

# For london - smaller dataset
# In [53]: r_row, p_value
# Out[53]: (-0.038325737277645697, 0.75454176074372548)

# For Edinburgh

# In [7]: r_row 
# Out[7]: -0.11382557906693604

# In [8]: p_value Out[8]: 0.34812122310798099


# For bankgkok 

# In [16]: r_row, p_value
# Out[16]: (-0.076801589460688977, 0.52743084103406335)

# For Paris

# In [18]: r_row, p_value
# Out[18]: (0.082348905898340055, 0.49794464126524751)


# For Manchester

# In [20]: r_row, p_value
# Out[20]: (0.083492130873147455, 0.47333843030568046)

# For Sydney

# In [23]: r_row, p_value
# Out[23]: (0.047154898428752631, 0.69198824802642978)


gradient, intercept, r_value, p_value, std_err = linregress(earches_and_tweets['Count'], earches_and_tweets['Searches'])

# In [45]: gradient
# Out[45]: 0.15605997434796715

# In [46]: intercept
# Out[46]: 11480.778176734118

# In [47]: r_value
# Out[47]: 0.13016098564086928

# In [48]: p_value
# Out[48]: 0.28283460745375744

# In [49]: std_err
# Out[49]: 0.14416035500838195
