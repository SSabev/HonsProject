import re
import json
import datetime
import csv
import glob, os, sys

class KeyStats(object):

    """
    This gives the data that is fed for the Aggregator.

    Word_counter is the one that does the words in text
    
    """
    
    def __init__(self, filename):

        self.filehandler = open(filename, 'rb')
        self.starttime = datetime.datetime.now()
        self.hashtags = {}
        self.get_keywords()
        # self.something_else
    
    def get_keywords(self):
        for line in self.filehandler:
            try:
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
            except ValueError:
                pass
            
    def to_csv(self, filename):
        outfile = open(filename, 'wb')
        outwriter = csv.writer(outfile)
        outwriter.writerow(['Hashtag', 'Datetime', 'TimesSeen'])
        for key in self.hashtags:
            data = self.hashtags[key]
            for i in data:
                outwriter.writerow([key.encode('ascii', 'ignore'), i.encode('ascii', 'ignore'), data[i]])

        outfile.close()



if __name__ == '__main__':
    current = 'data-dump-with-dt-28'
    all_the_files = [i for i in glob.glob(r'data-dump-with-*') if i != current]
    print all_the_files
    for i in all_the_files:
        filename = i.split('-')[-1]
        tags = KeyStats(i)

        delta = datetime.datetime.now() - tags.starttime
        tags.to_csv('%s.csv'%str(filename))
        print delta.seconds 
