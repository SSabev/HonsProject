import json
import datetime
import csv
import glob, os, sys
import pandas as p
import terms
import travelandcities as tc


class Aggregator(object):
    """
    This aggreagates hashtags and spits out the most popular place name hashtags
    """
    def __init__(self, filenames):

        self.filenames = filenames
        if type(filenames) == type([]):
            self.load_all()
        else:
            self.load_single()

    def load_all(self):
        dataframes = []
        for i in self.filenames:
            dataframes.append(p.read_csv(i))
        self.data = p.concat(dataframes)
        print self.data

    def load_single(self):
        self.data = p.read_csv(self.filenames)

    def get_tags(self):
        print len(self.data['Hashtag'])
        print len(set(self.data['Hashtag']))
        self.uniques = set(self.data['Hashtag'])

    def get_popular(self, directory):
        cities = tc.get_cities()
        done_tags = [i for i in glob.glob(r'hashtag/*.csv')]
        done_tags = [i.split('/')[1].split('.')[0] for i in done_tags]
        print done_tags
        for i in iter(self.uniques):
            if i not in done_tags and (i in cities or i in terms.terms):
                df = self.data[self.data['Hashtag'] == i]
                df_sum = sum([j for j in df['TimesSeen']])
                if df_sum > 100:
                    print i
                    df.to_csv('%s/%s.csv'%(directory,i))
                else:
                    pass
    

if __name__ == '__main__':
    all_the_files = [i for i in glob.glob(r'processed/*.csv')]
    print all_the_files

    f = 'travel_counts.csv'
    directory = 'travel_counts'
    a = Aggregator(f)
    a.get_tags()
    a.get_popular(directory)
