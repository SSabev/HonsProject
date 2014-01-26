import json
import datetime as dt 
import pandas as p
import numpy as np
from terms import terms 

class TopFeatures(object):
    def __init__(self, f, list_of_topics, dates_of_interest=None):
        self.f = open(f, 'rb')
        self.dates = dates_of_interest
        self.list_of_topics = list_of_topics
        self.travel = {}
        self.load_stopwords()
        self.crawl()
        self.create_dfs()

    def load_stopwords(self):
        self.stopwords = {}
        tempfile = open('tidydata/stopwords.txt')
        for line in tempfile:
            self.stopwords[line.strip()] = ''


    def crawl(self):
        self.j = 0
        for line in self.f:
            data = json.loads(line)
            text = data['text']
            for i in self.list_of_topics:
                if i.lower() in text.lower():
                    for token in text.split():
                        if token.lower() != i.lower() and token.lower() not in self.stopwords:
                            self.dict_count[token] = self.dict_count.get(token, 0) + 1
            for i in terms:

                if i.lower() in text.lower():
                    for token in text.split():
                        if token.lower() not in self.stopwords:
                            #dt_stamp = datetime.datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                            #dt_key = dt_stamp.strftime('%Y-%m-%d')
                            self.travel[token] = self.travel.get(token, 0) + 1
                            #if token not in self.keywords:
                            #    self.travel[token] = {}
                            #    self.keywords[token][dt_key] = self.keywords[token].get(dt_key, 0) + 1
                            #else:
                            #    self.keywords[token][dt_key] = self.keywords[token].get(dt_key, 0) + 1


            self.j+=1

            if self.j%100000 == 0:
                print "Finished %s tweets so far!"%str(self.j)
    
    def create_dfs(self):
        self.tdf = p.DataFrame(list(self.travel.iteritems()), 
                      columns=['TravelTerm', 'Count']).sort(columns=['Count'], ascending=False)

if __name__ == '__main__':
    f = 'data'
    topics = ['London']
    a = TopFeatures(f, topics)

    #a.tdf  = a.tdf.sort(columns = ['Count'], ascending=False)
    #a.df  = a.df.sort(columns = ['Count'], ascending=False)
