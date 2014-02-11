import json
import datetime as dt 
import csv
import pandas as p
import numpy as np
import terms
from dateutil.relativedelta import relativedelta
from Last4Fridays import Analyser

class ExitsProcessor(object):
    def __init__(self, filenames, directory):

        self.filenames = filenames
        self.directory = directory
        self.load_single()
        self.get_name_mapping()

    def get_name_mapping(self):
        f = open('tbcities.dat', 'r')
        self.cities = {}
        for line in f:
            temp = line.split('\t')
            name = temp[1]
            self.cities[temp[0]] = name
        return self.cities
    
    def load_single(self):
        self.data = p.read_csv(self.filenames)
        self.original = self.data
        print self.data

    def list_cities(self):
        print len(self.data['ToCity'])
        print len(set(self.data['ToCity']))
        self.uniques = set(self.data['ToCity'])
        
    def make_extracts_for_cities(self):
        bad, good = 0, 0
        del self.data['ToAirport']
        del self.data['ToCountry']
        for i in iter(self.uniques):
            if (i in self.cities):
                df = self.data[self.data['ToCity'] == i] 
                if sum(df['Exits'])>100:
                    df = df.groupby(['Date','ToCity'])
                    new_df = df.agg({'Searches': np.sum, 'Exits': np.sum}).reset_index()
                    del new_df['ToCity']
                    new_df.sort('Date',ascending=True, inplace=True) 
                    try:
                        st = dt.datetime.strptime('2013-10-30', "%Y-%m-%d")
                        en = st + relativedelta(days = 10)
                        while st < en:
                            temp = st.strftime('%Y-%m-%d')
                            new_df = new_df[new_df.Date != temp]
                            st += relativedelta(days = 1)
                        
                        new_df = new_df[new_df.Date != '2013-12-12']
                        a = Analyser(new_df)
                        a.backfill('Searches')
                        a.backfill('Exits')
                        a.results.Searches = a.results.Searches.astype('int')
                        a.results.Exits = a.results.Exits.astype('int')
                        del a.results['Forecast']
                        a.results.to_csv('%s/%s.csv'%(self.directory,self.cities[i].replace('/', '')), index=False)
                        #print "Finished successfully %s"%self.cities[i]
                        good += 1
                    except TypeError:
                        bad += 1

        print "%s finished successfully"%str(good)
        print "%s went tits up"%str(bad)

    def make_extracts_for_countries(self):
        bad, good = 0, 0
        del self.original['ToAirport']
        del self.original['ToCity']
        for i in iter(set(self.original['ToCountry'])):
            print i
            df = self.original[self.original['ToCountry'] == i] 
            if sum(df['Exits'])>100:
                df = df.groupby(['Date','ToCountry'])
                new_df = df.agg({'Searches': np.sum, 'Exits': np.sum}).reset_index()
                del new_df['ToCountry']
                new_df.sort('Date',ascending=True, inplace=True) 
                try:
                    st = dt.datetime.strptime('2013-10-30', "%Y-%m-%d")
                    en = st + relativedelta(days = 10)
                    while st < en:
                        temp = st.strftime('%Y-%m-%d')
                        new_df = new_df[new_df.Date != temp]
                        st += relativedelta(days = 1)
                    
                    new_df = new_df[new_df.Date != '2013-12-12']
                    a = Analyser(new_df)
                    a.backfill('Searches')
                    a.backfill('Exits')
                    a.results.Searches = a.results.Searches.astype('int')
                    a.results.Exits = a.results.Exits.astype('int')
                    del a.results['Forecast']
                    a.results.to_csv('%s/%s.csv'%(self.directory,i), index=False)
                    #print "Finished successfully %s"%self.cities[i]
                    good += 1
                except TypeError:
                    bad += 1

        print "%s finished successfully"%str(good)
        print "%s went tits up"%str(bad)

if __name__ == '__main__':
    f = 'searches.csv'
    directory = 'tidydata/se'
    a = ExitsProcessor(f, directory)
    a.list_cities()
    #a.make_extracts_for_cities()
    a.make_extracts_for_countries()

