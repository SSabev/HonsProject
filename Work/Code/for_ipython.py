# from detect_cusum import detect_cusum
# data = np.array(p.read_csv('../test_data/Sochi-weekly.csv').Searches.dropna().tolist())
#
# mean = np.median(data)
# drift = np.median(data)/2

# print data
#print data, mean, drift
#ta, tai, taf, amp = detect_cusum(data, mean, drift, True, True)


import pandas as p
import numpy as np
import math

data = np.array(p.read_csv('../test_data/Sochi-weekly.csv').Searches.dropna().tolist())
# data = np.array(p.read_csv('tidydata/joined/Sochi.csv').RMSearches.dropna().tolist())


no_more_changepoints = False

with open('../out.csv', 'w') as file:

    file.write("Index,Searches,MAX1\n")

    while not no_more_changepoints:
        mean = data.mean()
        stdev = data.std()

        for i in range(1, len(data)-1):
            mean1, mean2 = data[:i].mean(), data[i:].mean()
            num1 = (-1/(2*math.pow(stdev,2)))*(math.pow((data[i]-mean1)+(data[i-1]-mean1), 2))
            num2 = (-1/(2*math.pow(stdev,2)))*(math.pow((data[i]-mean2)+(data[i+1]-mean2), 2))

            file.write("%s,%s,%s\n" % \
                  (str(i), str(data[i]), max(num1,num2)))

        no_more_changepoints = True


data = p.read_csv('../out.csv')
