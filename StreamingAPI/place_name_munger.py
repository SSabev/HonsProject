import json
import datetime
import csv
import glob, os, sys
import pandas as p
import terms
import get_only_place_tweets as tc


class PlaceNameCounter(object):
    """
    This is similar to the aggregator but does not work with hashtags, but the text itself. 
    Thusly it gives slighly higher counts.
    """
    def __init__(self, filenames):

        self.filenames = filenames
        if type(filenames) == type([]):
            self.load_all()
        else:
            self.load_single()
        #self.get_median()

    def load_all(self):
        dataframes = []
        for i in self.filenames:
            dataframes.append(p.read_csv(i))
        self.data = p.concat(dataframes)
        print self.data

    def load_single(self):
        self.data = p.read_csv(self.filenames)

    def get_tags(self):
        print len(self.data['KeyWord'])
        print len(set(self.data['KeyWord']))
        self.uniques = set(self.data['KeyWord'])

    def get_popular(self, directory):
        cities = tc.get_cities()
        #done_tags = [i for i in glob.glob(r'tc/*.csv')]
        done_tags = [] #[i.split('/')[1].split('.')[0] for i in done_tags]
        print done_tags
        for i in iter(self.uniques):
            if i not in done_tags and (i in cities or i in terms.terms):
                df = self.data[self.data['KeyWord'] == i]
                df_sum = sum([j for j in df['Count']])
                if df_sum > 100:
                    print i
                    df.sort('Datetime',ascending=True, inplace=True) 
                    df.to_csv('%s/%s.csv'%(directory,i), index=False)
                else:
                    pass

if __name__ == '__main__':
    #all_the_files = [i for i in glob.glob(r'processed/*.csv')]
    #print all_the_files

    f = 'travel_counts.csv'
    directory = 'tc'
    a = PlaceNameCounter(f)
    a.get_tags()
    a.get_popular(directory)
