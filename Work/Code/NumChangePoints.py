__author__ = 'subevstefan'

import pandas as p
import numpy as np
import math
from detect_cusum import detect_cusum
import matplotlib.pyplot as plt

data = np.array(p.read_csv('tidydata/joined/Sochi.csv').RMSearches.dropna().tolist())

no_more_changepoints = False

print "Index,Searches,Number1,Number2,Ratio,MAX,Diff"

while not no_more_changepoints:
    mean = data.mean()
    stdev = data.std()

    for i in range(1, len(data)-1):
        mean1, mean2 = data[:i].mean(), data[i:].mean()
        num1 = (-1/(2*math.pow(stdev,2)))*(math.pow((data[i]-mean1)+(data[i-1]-mean1), 2))
        num2 = (-1/(2*math.pow(stdev,2)))*(math.pow((data[i]-mean2)+(data[i+1]-mean2), 2))
        try:
            ratio = math.fabs((max(num1,num2)-min(num1,num2))/max(num1,num2))
        except ZeroDivisionError:
            ratio = "10000"
        combined = num1 + num2
        diff = data[i]-data[i-1]
        print "%s,%s,%s,%s,%s,%s,%s" % \
              (str(i), str(data[i]), str(num1), str(num2), str(ratio), max(num1,num2),str(diff))

    no_more_changepoints = True