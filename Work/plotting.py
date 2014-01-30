import matplotlib.pyplot as plt
import pandas as p
import datetime as dt
import glob

def plot_city(city):
    """
    Simple small script for plotting timeseries
    """

    data = p.read_csv('tc/%s.csv'%city)

    data['Datetime'] = data['Datetime'].map(lambda x: dt.datetime.strptime(x,'%Y-%m-%d'))
    plt.title('Mentions of %s on Twitter'%city)
    plt.plot(data['Datetime'], data['Count'])
    plt.show()

def plot_exits(city):
    """
    This bit here will plot the exits/searches
    """
    data = p.read_csv('Exits/%s.csv'%city)

    data['Date'] = data['Date'].map(lambda x: dt.datetime.strptime(x,'%Y-%m-%d'))
    data['Exits'] = data['Exits'].map(lambda x: int(x))

    plt.plot(data['Date'], data['Exits'])
    plt.show()


if __name__ == '__main__':
    keyword_files = [i for i in glob.glob('tc/*csv')]
    top_n = []
    for i in keyword_files:
        data = p.read_csv(i)
        top_n.append((sum(data['Count']), i.split('/')[-1].replace('.csv','')))

    top_n = sorted(top_n, reverse=True)
    for i, j in top_n[:12]:
        print "%s %s"%(j, i)
        plot_city(j)


