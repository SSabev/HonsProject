import pandas as p
from scipy.stats import pearsonr, linregress
import glob
import matplotlib.pyplot as plt
import pylab


test_values = {}
city = 'Sochi'

for i in glob.glob('tidydata/joined/*csv'):
    data = p.read_csv(i)

    data = data.dropna()
    r_value, p_value = pearsonr(data['Count'], data['NSearches'])
    city = i.split('/')[-1].replace('.csv', '')

    test_values[city] = {
                            'R value': r_value,
                            'P value': p_value
                        }


values_df = p.DataFrame.from_dict(test_values, orient="index")
values_df.to_csv('correlations.csv')


#plt.scatter(searches_and_tweets['Count'], searches_and_tweets['NSearches'])
#plt.title('Scatter of twitter counts against searches for %s'%city)
#plt.xlabel(r"Twitter counts", fontsize = 12)
#plt.ylabel(r"Search count (Normalised)", fontsize = 12)
#pylab.show()
#
#print (r_value, p_value)
