import matplotlib.pyplot as plt
import pandas as p
import datetime as dt

"""
Simple small script for plotting timeseries
"""

city = 'Bangkok'

data = p.read_csv('tc/%s.csv'%city)

data['Datetime'] = data['Datetime'].map(lambda x: dt.datetime.strptime(x,'%Y-%m-%d'))

plt.plot(data['Datetime'], data['Count'])
plt.show()


"""
This bit here will plot the exits/searches
"""


city = 'London'

data = p.read_csv('Exits/%s.csv'%city)

data['Date'] = data['Date'].map(lambda x: dt.datetime.strptime(x,'%Y-%m-%d'))
data['Exits'] = data['Exits'].map(lambda x: int(x))

plt.plot(data['Date'], data['Exits'])
plt.show()
