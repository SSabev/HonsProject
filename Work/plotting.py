import matplotlib.pyplot as plt
import pandas as p
import datetime as dt
import glob

def plot_both(city):
    """
    Simple small script for plotting timeseries
    """
    try:
        data = p.read_csv('tidydata/joined/%s.csv'%city)

        def apply_dt(row):
            if len(row) > 10:
                return dt.datetime.strptime(row, '%Y-%m-%d %H:%M:%S')
            else:
                return dt.datetime.strptime(row, '%Y-%m-%d')
        data['Date'] = data['Date'].apply(apply_dt) 

        plt.figure(1)
        plt.subplot(211)
        plt.title('Mentions of %s on Twitter'%city)
        plt.plot(data['Date'], data['Count'])
        plt.xlabel(r"Date", fontsize = 12)
        plt.ylabel(r"Search count (Normalised)", fontsize = 12)

        plt.subplot(212)
        plt.title('Searches to %s'%city)
        plt.plot(data['Date'], data['NSearches'])
        plt.xlabel(r"Date", fontsize = 12)
        plt.ylabel(r"Twitter counts", fontsize = 12)
        plt.show()

        plt.scatter(data['Count'], data['NSearches'])
        plt.title('Scatter of twitter counts against searches for %s'%city)
        plt.xlabel(r"Twitter counts", fontsize = 12)
        plt.ylabel(r"Search count (Normalised)", fontsize = 12)
        plt.show()
    except IOError:
        print "no such place"

    

def plot_exits(city):
    """
    This bit here will plot the exits/searches
    """
    data = p.read_csv('tidydata/se/%s.csv'%city)

    data['Date'] = data['Date'].map(lambda x: dt.datetime.strptime(x,'%Y-%m-%d %H:%M%:%S'))
    data['Exits'] = data['Exits'].map(lambda x: int(x))

    plt.plot(data['Date'], data['Exits'])
    plt.show()


if __name__ == '__main__':
    keyword_files = [i for i in glob.glob('tidydata/joined/*csv') if 'London' in i]
    top_n = []
    for i in keyword_files:
        data = p.read_csv(i)
        top_n.append((sum(data['Count']), i.split('/')[-1].replace('.csv','')))

    top_n = sorted(top_n, reverse=True)
    for i, j in top_n[:20]:
        print "%s %s"%(j, i)
        plot_both(j)


