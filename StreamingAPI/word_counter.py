import re
import json
import datetime
import csv
from terms import terms
import travelandcities as tc


class WordCounter(object):
    """
    Pretty much copy of the keywords_cruncher. Only difference is this gives you words, not hashtag counts
    """
    
    def __init__(self, filename):

        self.filehandler = open(filename, 'rb')
        self.starttime = datetime.datetime.now()
        self.keywords = {}
        self.get_keywords()
        # self.something_else
    
    def get_keywords(self):
        cities = tc.get_cities()
        for line in self.filehandler:
            try:
                data = json.loads(line)
                if 'text' in data:
                    for token in data['text'].split(' '):
                        if token in cities or token in terms:
                            dt_stamp = datetime.datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                            dt_key = dt_stamp.strftime('%Y-%m-%d')
                            if token not in self.keywords:
                                self.keywords[token] = {}
                                self.keywords[token][dt_key] = self.keywords[token].get(dt_key, 0) + 1
                            else:
                                self.keywords[token][dt_key] = self.keywords[token].get(dt_key, 0) + 1
            except ValueError:
                pass
            
    def to_csv(self, filename):
        outfile = open(filename, 'wb')
        outwriter = csv.writer(outfile)
        outwriter.writerow(['KeyWord', 'Datetime', 'Count'])
        for key in self.keywords:
            data = self.keywords[key]
            for i in data:
                outwriter.writerow([key.encode('ascii', 'ignore'), i.encode('ascii', 'ignore'), data[i]])

        outfile.close()



if __name__ == '__main__':

    b = WordCounter('data')
    b.to_csv('travel_counts.csv')
    
    
