import json
import datetime
import csv
from terms import terms, countries
import pandas as p
import glob
import io
import nltk
import string
import numpy as np

class FeatureExtractor(object):

    """
    """
    def __init__(self, basepath):
        print glob.glob('tidydata/features/*')
        self.processed  = []
        for line in open('tidydata/features_status'):
            self.processed .append(line)
        print self.processed 
        print "Processed %s files so far"%str(len(self.processed))
        self.all_the_files = [i for i in glob.glob(r'%s/*'%basepath) if i not in self.processed]
        print self.all_the_files
        print "Got %s files to go through"%str(len(self.all_the_files))
        self.process_files()
        #self.process_the_counts()

    def convert_timedelta(self, duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return hours, minutes, seconds

    def get_cities(self):
        f = open('tbcities.dat', 'r')
        cities = {}
        for line in f:
            temp = line.split('\t')
            name = temp[1]
            cities[name.lower()] = ''
        return cities

    def get_lists(self):
        self.geotokens = self.get_cities()
        for i in countries:
            self.geotokens[i] = ''
        return self.geotokens


    def process_files(self):
        self.startime = None
        self.get_lists()
        self.counts = {}
        self.counts['london'] = {}
        #for i in self.geotokens:
        #    self.counts[i] = {}


        for twfile in self.all_the_files:
            self.starttime = datetime.datetime.now()
            print "I have just started %s"%twfile
            for line in open(twfile, 'r'):
                change = False
                travelFlag = False
                try:
                    tweet = json.loads(line)
                except ValueError:
                    print "Faulty tweet"
                    
                if tweet:
                    temp = tweet['text'].encode('utf-8').lower().replace('\n', ' ')
                    dt_stamp = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    dt_key = dt_stamp.strftime('%Y-%m-%d')
                    tokens = temp.split(' ')
                    
                    #to_traverse = []
                    #for i in self.geotokens:
                    #    if i in temp:
                    #to_traverse.append(i)
                    
                    #for geot in to_traverse:
                    #    for token in temp.split(' '):
                    #        dictemp = self.counts[geot].get(token, {})
                    #        dictemp[dt_key] = dictemp.get(dt_key, 0) + 1
                    #       self.counts[geot][token] = dictemp

                    if 'london' in temp:
                        for token in temp.split(' '):
                            if 'http' not in token and '@' not in token:
                                dictemp = self.counts['london'].get(token, {})
                                dictemp[dt_key] = dictemp.get(dt_key, 0) + 1
                                self.counts['london'][token] = dictemp

                

            h, m, s = self.convert_timedelta(datetime.datetime.now() - self.starttime)
            print '{} took {}h,{}m,{}s to process'.format(twfile, h, m, s)
            self.startime = datetime.datetime.now()

    def process_the_counts(self):
        for i in self.counts:
            data = p.DataFrame.from_dict(self.counts[i])
            print data
            sums = {}
            for i in data.columns:
                sums[i] = np.sum(data[i])
            sorted_sums=sorted(sums.iteritems(), key=lambda x: x[1], reverse=True)
            sorted_sums = [(i, j) for (i, j) in sorted_sums if "@" not in i and \
                    'http' not in i and i not in nltk.corpus.stopwords('english') and i not in string.punctuation]
            to_keep = []
            for i in sorted_sums[:500]:
                to_keep.append(i)
            for i in data.columns:
                if i not in to_keep:
                    del data['%s'%i]
            data.to_csv('%s.features.csv'%i.capitalize())

if __name__ == '__main__':
    basepath2 = '/Volumes/Samsung/traveltweets_expanded'
    basepath = "traveltweets_expanded"
    a = FeatureExtractor(basepath)

