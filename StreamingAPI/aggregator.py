import json
import datetime
import csv
import glob, os, sys
import pandas as p


class Aggregator(object):

    def __init__(self, filenames):

        self.filenames = filenames
        self.load()
        self.get_tags()
        self.get_popular()

    def load(self):
        dataframes = []
        for i in self.filenames:
            dataframes.append(p.read_csv(i))

        self.data = p.concat(dataframes)
        print self.data

    def get_tags(self):
        print len(self.data['Hashtag'])
        print len(set(self.data['Hashtag']))

    def get_popular(self):

        df = self.data.groupby('Hashtag')
        df.sum()

        df.to_csv('temp.csv')

if __name__ == '__main__':
    all_the_files = [i for i in glob.glob(r'processed/*.csv')]
    print all_the_files

    a = Aggregator(all_the_files)
