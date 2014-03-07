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
        with open('tidydata/file_status', 'r') as f:
            for line in f:
                self.processed.append(line.rstrip())

        self.to_process = todo
        print self.to_process
        print "Processed %s files so far"%str(len(self.processed))
        self.all_the_files = [i for i in glob.glob(r'%s/*'%basepath)]
        self.all_the_files = sorted(list(set(self.all_the_files).difference(set(self.processed))))
        print self.all_the_files

        if self.all_the_files:
            self.process_files()
            self.merge_all()
        else:
            self.merge_all()
            print "All the files are done"

        self.output_processed()

    def convert_timedelta(self, duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return hours, minutes, seconds

    def get_cities(self):
        cities = {}
        with open('tbcities.dat', 'r') as f:
            for line in f:
                temp = line.split('\t')
                name = temp[1]
                cities[name.lower()] = ''
        return cities

    def get_lists(self):
        self.geotokens = self.get_cities()
        for i in countries:
            self.geotokens[i.lower()] = ''
        return self.geotokens


    def process_files(self):
        self.startime = None
        self.get_lists()
        self.punctuation = string.punctuation.replace('#', '')
        self.punctuation += '\r\n\t'
        print self.punctuation

        for twfile in self.all_the_files:
            self.counts = {}
            for city in self.to_process:
                self.counts[city] = {}

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
                        if city in temp:
                            for token in temp.split(' '):
                                if 'http' not in token and '@' not in token:
                                    dictemp = self.counts[city].get(token, {})
                                    dictemp[dt_key] = dictemp.get(dt_key, 0) + 1
                                    self.counts[city][token] = dictemp

            #print self.counts.keys()
            for key in self.counts:
                to_keep = {}
                for i in self.counts[key]:
                    if i not in nltk.corpus.stopwords.words('english') and i != '':
                        temp = i
                        translated = temp.translate(None, self.punctuation)
                        to_keep[translated] = self.counts[key][i]

                #print key, self.counts.get(key).keys()[:10]
                #print len(self.counts.get(key).keys())
                #print len(to_keep.keys())
                data = p.DataFrame.from_dict(to_keep)
                data.to_csv('rawfeatures/%s-%s.csv'%(key, twfile.split('-')[-1]))

                #h, m, s = self.convert_timedelta(datetime.datetime.now() - self.starttime)
                #print '{} took {}h,{}m,{}s to process'.format(key, h, m, s)
                #self.startime = datetime.datetime.now()

            h, m, s = self.convert_timedelta(datetime.datetime.now() - self.starttime)
            print '{} took {}h,{}m,{}s to process'.format(twfile, h, m, s)

            self.processed.append(twfile)

    def merge_all(self):
        for city in self.to_process:
            csvs = glob.glob(r'rawfeatures/%s*.csv'%city)

            data = p.DataFrame()
            for i in csvs:
                print i
                data = data.append(p.read_csv(i))
            data['Date'] = data['Unnamed: 0']
            try:
                del data['Unnamed: 0']
                del data['Unnamed: 1']
            except ValueError:
                pass
            data = data.groupby(['Date'])
            data = data.sum()
            data.to_csv('tidydata/rawfeatures/%s.csv'%city)

    def output_processed(self):
        with open('tidydata/file_status', 'w') as f:
            for i in self.processed:
                f.write('%s\n'%i)

if __name__ == '__main__':
    basepath2 = '/Volumes/Samsung/traveltweets'
    basepath = "traveltweets"

    places = []
    with open('tidydata/places_list') as f:
        for line in f:
            places.append(line.rstrip().lower())
    print places
    a = FeatureExtractor(basepath, places)
