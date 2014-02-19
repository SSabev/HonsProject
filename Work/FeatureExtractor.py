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
    def __init__(self, basepath, todo):
        self.processed  = []
        self.to_process = todo
        with open('tidydata/features_status', 'r') as f:
            for line in f:
                self.processed.append(line.rstrip())

        print "Processed %s cities so far"%str(len(self.processed))
        print self.processed
        print self.to_process
        self.to_process = set(self.to_process).difference(set(self.processed))
        self.all_the_files = [i for i in glob.glob(r'%s/*'%basepath)]
        print "Got %s cities to go through"%str(len(self.to_process))
        if self.to_process:
            self.process_files()
        else:
            print "All the cities are done"

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
        for city in self.to_process:
            self.counts[city] = {}


        for twfile in self.all_the_files:
            self.starttime = datetime.datetime.now()
            print "I have just started %s"%twfile
            for line in open(twfile, 'r'):
                try:
                    tweet = json.loads(line)
                except ValueError:
                    print "Faulty tweet"
                    
                if tweet:
                    temp = tweet['text'].encode('utf-8').lower().replace('\n', ' ')
                    dt_stamp = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    dt_key = dt_stamp.strftime('%Y-%m-%d')
                    tokens = temp.split(' ')

                    for city in self.to_process:
                        for token in temp.split(' '):
                            if 'http' not in token and '@' not in token:
                                dictemp = self.counts[city].get(token, {})
                                dictemp[dt_key] = dictemp.get(dt_key, 0) + 1
                                self.counts[city][token] = dictemp

            h, m, s = self.convert_timedelta(datetime.datetime.now() - self.starttime)
            print '{} took {}h,{}m,{}s to process'.format(twfile, h, m, s)
            self.startime = datetime.datetime.now()

        for city in self.to_process:
            self.process_and_output(city)

        self.output_to_file_process()


    def process_and_output(self, name):
        data = self.counts.get(name)
        sums = {}
        for word in self.counts.get(name):
            sums[word] = np.sum([j for (i, j) in self.counts.get(name)[word].iteritems()])
        
        sorted_sums=sorted(sums.iteritems(), key=lambda x: x[1], reverse=True)
        sorted_sums = [(i.translate(None, string.punctuation), j) for (i, j) in sorted_sums]
        sorted_sums = [(i, j) for (i, j) in sorted_sums if i not in nltk.corpus.stopwords.words('english') and i != '']

        best_features = {i:'' for (i,j) in sorted_sums[:500]}
        kept = {}
        for feature in best_features:
            kept[feature] = self.counts.get(name).get(feature)


        kept = p.DataFrame.from_dict(kept)
        kept = kept.fillna(0)
        kept.to_csv('tidydata/rawfeatures/%s.csv'%name)
        self.processed.append(name)
    
    def output_to_file_process(self):
        with open('tidydata/features_status', 'w') as f:
            for i in self.processed:
                f.write('%s\n'%i)
    
if __name__ == '__main__':
    basepath2 = '/Volumes/Samsung/traveltweets_expanded'
    basepath = "traveltweets_expanded"

    list_of_todo = ['london', 'paris']
    a = FeatureExtractor(basepath, list_of_todo)

