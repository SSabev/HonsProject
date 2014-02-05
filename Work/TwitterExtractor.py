import json
import datetime
import csv
from terms import terms, countries
import pandas as p
import glob


class TwitterExtractor(object):

    """
    2014-02-04 - Stefan
    Tidying up the mess I left with all of the three files. That requires to do one linear sweep on the
    big set and then another one on the smaller set.
    This will mitigate it, but bringing everything together and hopefully making it a bit more flexible. 
    And it will use more pandas rather than all the other custom crap.
    """
    def __init__(self, basepath):
        self.processed = ["%s/%s"%(basepath,i.split('/')[-1]) for i in glob.glob('traveltweets_expanded/*')]
        print "Processed %s files so far"%str(len(self.processed))
        self.all_the_files = [i for i in glob.glob(r'%s/data-dump-with-dt-*'%basepath) if i not in self.processed]
        print "Got %s files to go through"%str(len(self.all_the_files))
        self.process_files()

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
        cities = self.get_cities()
        multi_word_cities = [i.lower() for i in cities if len(i.split(' ')) >= 2]
        multi_word_countries = [i.lower() for i in countries if len(i.split(' ')) >= 2]
        single_word_countries = [i.lower() for i in countries if len(i.split(' ')) < 2]

        single_word_cities = set(cities).difference(set(multi_word_cities))
        single_word_countries = set(single_word_countries)

        self.single_word = single_word_cities.union(single_word_countries)
        self.multi_word = multi_word_cities + multi_word_countries

        del multi_word_cities, multi_word_countries, single_word_cities, single_word_countries

    def process_files(self):
        self.startime = None
        cities = self.get_cities()
        self.get_lists()
        for twfile in self.all_the_files:
            change = False
            travelFlag = False
            self.starttime = datetime.datetime.now()
            print "I have just started %s"%twfile
            self.counts = {}
            for i in self.single_word:
                self.counts[i] = {}
            for i in self.multi_word:
                self.counts[i] = {}

            self.counts['Brazil'] = {}
            filename_current = twfile.split('/')[-1]
            outfile = open('traveltweets_expanded/%s'%filename_current, 'wb')

            for line in open(twfile, 'r'):
                try:
                    tweet = json.loads(line)
                except ValueError:
                    print "Faulty tweet"
                    
                if tweet:
                    temp = tweet['text'].encode('utf-8').lower()
                    for w in terms:
                        if w in temp:
                            travelFlag = True
                            break

                    dt_stamp = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    dt_key = dt_stamp.strftime('%Y-%m-%d')
                    if 'rio' in temp or 'brazil' in temp or 'world cup' in temp:
                        change = True
                        self.counts['Brazil'][dt_key] = self.counts['Brazil'].get(dt_key, 0) + 1

                    for i in self.multi_word:
                        if i in temp:
                            change = True
                            if travelFlag:
                                self.counts[i][dt_key] = self.counts[i].get(dt_key, 0) + 1

                    for token in temp.split(' '):
                        if token in self.single_word:
                            change = True
                            if travelFlag:
                                self.counts[i][dt_key] = self.counts[i].get(dt_key, 0) + 1

                    if change and travelFlag and tweet:
                        outfile.write(json.dumps(tweet) + '\n')

            for key in self.counts:
                temp = self.counts[key]
                print list(temp.iteritems())
                df = p.DataFrame(list(temp.iteritems()), \
                columns=['Date', 'Count']).sort(columns=['Date'], ascending=False)
                df.to_csv('pcounts/%s.csv'%str(key))
                               
            
            h, m, s = self.convert_timedelta(datetime.datetime.now() - self.starttime)
            print '{} took {}h,{}m,{}s to process'.format(twfile, h, m, s)
            self.startime = datetime.datetime.now()




if __name__ == '__main__':

    basepath = "/Volumes/Tweets/Data"
    a = TwitterExtractor(basepath)


