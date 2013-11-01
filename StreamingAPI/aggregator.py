import json
import datetime
import csv
import glob, os, sys
import pandas as p


class Aggregator(object):

    def __init__(self, filenames):

        self.filenames = filenames
        self.load()
            
    def load(self):
        dataframes = []
        for i in self.filenames:
            dataframes.append(p.read_csv(i))

        self.data = p.concat(dataframes)

if __name__ == '__main__':
    all_the_files = [i for i in glob.glob(r'processed/*.csv')]
    print all_the_files

    a = Aggregator(all_the_files)
