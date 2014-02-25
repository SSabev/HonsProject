import json
import datetime
import csv
import glob, os, sys
import pandas as p

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
    
    def get_keywords(self):
        for line in self.filehandler:
            try:
                data = json.loads(line)
                if 'entities' in data:
                    hastags = data['entities']['hashtags']
                    dt_stamp = datetime.datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

                    dt_key = dt_stamp.strftime('%Y-%m-%d')
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
        outwriter.writerow(['Tag', 'Date', 'Count'])
        for key in self.hashtags:
            data = self.hashtags[key]
            for i in data:
                outwriter.writerow([key.encode('ascii', 'ignore'), i.encode('ascii', 'ignore'), data[i]])

        outfile.close()

if __name__ == '__main__':
    all_the_files = [i for i in glob.glob(r'traveltweets_expanded/data-dump-with-*')]
    print all_the_files



    for i in all_the_files:
        filename = i.split('-')[-1]
        tags = KeyStats(i)

        delta = datetime.datetime.now() - tags.starttime
        tags.to_csv('hashtags/raw/%s.csv'%str(filename))
        print delta.seconds 

    data = p.DataFrame()
    for i in glob.glob('hashtags/raw/*.csv'):
        data.append(p.read_csv(i))

    tags = list(set(data.Tag))
    for i in tags[1:]:
        temp = data[data.Tag == i]
        temp.to_csv('hashtags/%s.csv'%i.replace('#', ''))
