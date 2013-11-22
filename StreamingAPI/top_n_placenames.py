import re
import json
from collections import Counter, OrderedDict
from travelandcities import get_cities

class TMCounter(object):

    def __init__(self):

        self.counter = {}

        pass
    
    def add_times(self,key, times):

        for i in add_times:
            pass
            


def process_file(infile):
    tokens = Counter()

    for line in infile:
        #print line
        try:

            data = json.loads(line)
        except ValueError:
            pass
        if 'text' in data:
            for token in data['text'].split(' '):
                tokens[token] += 1
    
    return tokens

if __name__ == "__main__":
    f = open('data', 'rb')
    t = process_file(f)
    print t
    f.close()

    cities = get_cities()
    final = {}
    for i,j in t.most_common(10000):
        if i in cities:
            final[i] = j


    output = open('derp', 'wb')
    output.write(json.dumps(OrderedDict(sorted(final.items(), key=lambda t: t[1], reverse=True)), indent=4))
    output.close()

    # data['Datetime'] = data['Datetime'].map(lambda x: x[:10])
    # data['TimesSeen'] = data['TimesSeen'].map(lambda x: int(x))
