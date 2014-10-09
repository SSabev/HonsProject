import json
import datetime as dt
import csv
import pandas as p
import numpy as np
import terms
import glob
from dateutil.relativedelta import relativedelta
from Last4Backfill import Analyser

class TwitterProcessor(object):
    def __init__(self, filenames, directory):
        self.filenames = filenames
        self.directory = directory
        self.backfill()

    def mergedfs(self, data):

        start = dt.datetime.strptime(data.Date.irow(0), '%Y-%m-%d')
        lastdate = dt.datetime.strptime(data.Date.irow(-1), '%Y-%m-%d')
        currentdate = start
        daterange = []
        while currentdate <= lastdate:
            daterange.append(currentdate)
            currentdate = currentdate + relativedelta(days = 1)

        new_df = p.DataFrame({
            "Date" : daterange})
        new_df.Date = new_df.Date.apply(lambda x: str(x)[:10])
        data.Date = data.Date.apply(lambda x: str(x))
        new_df = new_df.merge(data, how="outer")
        return new_df


    def backfill(self):
        def conversion(date):
            return dt.datetime.strptime(date[:10], '%Y-%m-%d')
        def backwards_conversion(date):
            return date.strftime('%Y-%m-%d')
        bad, good = 0, 0
        for filename in self.filenames:
            print filename
            name = filename.split('/')[-1].replace('.csv','')
            data = p.read_csv(filename)
            data.to_csv('%s/%s.csv'%(directory,name), index=False)
            # if np.sum(data.Count) > 100:
            #     if 'Datetime' in data.columns:
            #         data['Date'] = data.Datetime
            #         del data['Datetime']
            #         del data['KeyWord']
            #
            #     data = data[data.Date != '2013-10-03']
            #     data = data[data.Date != '2013-10-15']
            #     data = data[data.Date != '2013-12-20']
            #     data = data[data.Date != '2013-12-27']
            #     data = data[data.Date != '2014-02-19']
            #     data = data[data.Date != '2014-01-25']
            #     data = data[data.Date != '2013-12-22']
            #     data = data[data.Date != '2013-11-22']
            #
            #     new_df = self.mergedfs(data)
            #     #new_df = new_df.fillna()
            #     if np.sum(data.Count) > 1000:
            #         new_df.Count = new_df.Count.interpolate()
            #     else:
            #         new_df = new_df.fillna(0)
            #     new_df.Count = new_df.Count.astype('int')
            #     new_df.Date = new_df.Date.apply(conversion)
            #     new_df.sort('Date',ascending=True, inplace=True)
            #     a = Analyser(new_df)
            #     a.backfill('Count')
            #     a.results.Count = a.results.Count.astype('int')
            #     del a.results['Forecast']
            #     a.results.to_csv('%s/%s.csv'%(directory,name), index=False)
            #     #print "Finished successfully %s"%self.cities[i]
            #     good += 1
            #except TypeError:
            #    bad += 1

        # print "%s finished successfully"%str(good)
        # print "%s went tits up"%str(bad)

if __name__ == '__main__':
    input_files = glob.glob('twittercounts/*.csv')
    directory = 'tidydata/twitter'
    a = TwitterProcessor(input_files, directory)
