import re
import json
import datetime
import csv
import glob, os, sys

class KeyStats(object):
    
    def __init__(self, filename):

        self.filehandler = open(filename, 'rb')
        self.starttime = datetime.datetime.now()
        self.hashtags = {}
        self.get_keywords()
        # self.something_else
    
    def get_keywords(self):
        for line in self.filehandler:
            data = json.loads(line)
            if 'entities' in data:
                hastags = data['entities']['hashtags']
                dt_stamp = datetime.datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

                dt_key = dt_stamp.strftime('%Y-%m-%d %H')
                for hashtag in hastags:
                    text = hashtag['text']
                    if text not in self.hashtags:
                        self.hashtags[text] = {}
                        self.hashtags[text][dt_key] = self.hashtags[text].get(dt_key, 0) + 1
                    else:
                        self.hashtags[text][dt_key] = self.hashtags[text].get(dt_key, 0) + 1

    def dump_tags(self):

        print self.hashtags
    
    def to_csv(self, filename):
        outfile = open('outfile.csv', 'wb')
        outwriter = csv.writer(outfile)
        outwriter.writerow(['Hashtag', 'Datetime', 'TimesSeen'])
        for key in self.hashtags:
            data = self.hashtags[key]
            for i in data:
                outwriter.writerow([key.encode('ascii', 'ignore'), i.encode('ascii', 'ignore'), data[i]])

        outfile.close()



if __name__ == '__main__':

    all_the_files = sorted(set([i for i in glob.glob(r'data-dump-with-*')][:-1]))
    print all_the_files
    for i, j in zip(all_the_files, xrange(0, len(all_the_files)-1)):
        tags = KeyStats(i)

        delta = datetime.datetime.now() - tags.starttime
        tags.to_csv('%s.csv'%str(j))
        print delta.seconds 
