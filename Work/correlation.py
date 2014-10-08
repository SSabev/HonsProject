import glob
import pandas as p
import numpy as np
from scipy.stats import pearsonr, linregress

test_values = {}
# place = 'Sochi'

for i in glob.glob('tidydata/joined/*csv'):
    data = p.read_csv(i)

    data = data.dropna()

    r_value, _ = pearsonr(data.RMCount, data.RMSearches)
    r_value_2, _ = pearsonr(data.Count, data.Searches)
    place = i.split('/')[-1].replace('.csv', '')

    test_values[place] = {
        'R value': r_value_2,
        'R smooth': r_value,
        'Searches Median': data.Searches.median(),
        'Searches StDev': data.Searches.std(),
        'Tweets Median': data.Count.median(),
        'Tweets StDev': data.Count.std(),
        'R diff': r_value-r_value_2,
    }

values_df = p.DataFrame.from_dict(test_values, orient="index")
values_df.to_csv('correlations.csv')


# plt.scatter(searches_and_tweets['Count'], searches_and_tweets['NSearches'])
#plt.title('Scatter of twitter counts against searches for %s'%place)
#plt.xlabel(r"Twitter counts", fontsize = 12)
#plt.ylabel(r"Search count (Normalised)", fontsize = 12)
#pylab.show()
#
#print (r_value, p_value)
