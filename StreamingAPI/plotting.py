import matplotlib.pyplot as plt
import pandas as p
import datetime as dt

"""
Simple small script for plotting timeseries
"""

city = 'London'

data = p.read_csv('tc/%s.csv'%city)

data['Datetime'] = data['Datetime'].map(lambda x: dt.datetime.strptime(x,'%Y-%m-%d'))

plt.plot(data['Datetime'], data['Count'])
plt.show()
