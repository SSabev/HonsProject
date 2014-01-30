import json
import datetime as dt 
import csv
import pandas as p
import numpy as np
import terms
import glob
from dateutil.relativedelta import relativedelta
from Last4Fridays import Analyser

class TwitterProcessor(object):
    def __init__(self, filenames, directory):

        self.filenames = filenames
        self.directory = directory
        self.backfill()

    def mergedfs(self, data):
        
        start = data.Date.irow(0)
        lastdate = data.Date.irow(-1)
        currentdate = start
        daterange = []
        while currentdate <= lastdate:
            daterange.append(currentdate)
            currentdate = currentdate + relativedelta(days = 1)
 
        new_df = p.DataFrame({
            "Date" : daterange})
        new_df = new_df.merge(data, how="outer")
        return new_df

    def backfill(self):
        def conversion(date):
            return dt.datetime.strptime(date, '%Y-%m-%d')
        def backwards_conversion(date):
            return date.strftime('%Y-%m-%d')
        bad, good = 0, 0
        for filename in self.filenames: 
            print filename
            name = filename.split('/')[-1].replace('.csv','')
            data = p.read_csv(filename)
            if np.sum(data.Count) > 100:
                data['Date'] = data.Datetime.apply(conversion)
                data = data[data.Date != '2013-10-03']
                data = data[data.Date != '2013-10-15']
                del data['KeyWord']
                del data['Datetime']
                new_df = self.mergedfs(data)
                new_df = new_df.fillna(new_df.mean())
                new_df.Count = new_df.Count.astype('int')
                new_df.Date = new_df.Date.apply(backwards_conversion)
                new_df.sort('Date',ascending=True, inplace=True) 

                #try:              
                new_df = new_df[new_df.Date != '2013-12-20']
                new_df = new_df[new_df.Date != '2013-12-27']
                
                
                a = Analyser(new_df)
                a.backfill('Count')
                a.results.Count = a.results.Count.astype('int')
                del a.results['Forecast']
                a.results.to_csv('%s/%s.csv'%(directory,name), index=False)
                #print "Finished successfully %s"%self.cities[i]
                good += 1
            #except TypeError:
            #    bad += 1

        print "%s finished successfully"%str(good)
        print "%s went tits up"%str(bad)

if __name__ == '__main__':
    input_files = glob.glob('tc/*.csv')
    directory = 'tidydata/twitter'
    a = TwitterProcessor(input_files, directory)
    
