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
        self.dict_count = {}
        self.travel = {}
        self.crawl()

    def crawl(self):
        for line in self.f:
            data = json.loads(line)
            text = data['text']
            for i in self.list_of_topics:
                if i.lower() in text.lower():
                    for token in text.split():
                        self.dict_count[token] = self.dict_count.get(token, 0) + 1
            for i in terms:
                if i.lower() in text.lower():
                    for token in text.split():
                        self.travel[token] = self.travel.get(token, 0) + 1

        self.df = p.DataFrame(list(self.dict_count.iteritems()),
                      columns=['Term','Count'])
        self.tdf = p.DataFrame(list(self.travel.iteritems()), 
                      columns=['TravelTerm', 'Count'])

        self.tdf = self.tdf.sort(columns=['Count'], ascending=False)
        self.df = self.df(columns=['Sort'], ascending=False)



if __name__ == '__main__':
    f = 'data'
    topics = ['London']
    a = TopFeatures(f, topics)
