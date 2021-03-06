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
        self.processed = ["%s/%s"%(basepath,i.split('/')[-1]) for i in glob.glob('/Volumes/Samsung/traveltweets/*')]
        print "Processed %s files so far"%str(len(self.processed))
        self.all_the_files = [i for i in glob.glob(r'%s/data-dump-with-dt-*'%basepath) if i not in self.processed]
        self.all_the_files.sort()
        print "Got %s files to go through"%str(len(self.all_the_files))
        print self.all_the_files

        self.process_files()
        self.rebalance_counts()

    def convert_timedelta(self, duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return hours, minutes, seconds

    def get_cities(self):
        f = open('../tbcities.dat', 'r')
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
        cities = self.get_cities()
        self.get_lists()
        self.counts = {}
        self.counts['Brazil'] = {}
        for i in self.single_word:
            self.counts[i] = {}
        for i in self.multi_word:
            self.counts[i] = {}

        for twfile in self.all_the_files[:1]:
            print "I have just started %s"%twfile
            filename_current = twfile.split('/')[-1]
            outfile = open('/Volumes/Samsung/traveltweets/%s'%filename_current, 'wb')
            for line in open(twfile, 'r'):
                change = False
                travelflag = False
                tweet = None
                try:
                    tweet = json.loads(line)
                except ValueError:
                    print "Faulty tweet"

                if tweet and 'text' in tweet.keys() and 'created_at' in tweet.keys():
                    temp = tweet['text'].encode('utf-8').lower()
                    for w in terms:
                        if w in temp:
                            travelflag = True
                            break

                    try:
                        dt_stamp = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                        dt_key = dt_stamp.strftime('%Y-%m-%d')
                    except:
                        pass

                    if 'world cup' in temp:
                        change = True
                        self.counts['Brazil'][dt_key] = self.counts['Brazil'].get(dt_key, 0) + 1

                    for i in self.multi_word:
                        if i in temp:
                            change = True
                            self.counts[i][dt_key] = self.counts[i].get(dt_key, 0) + 1

                    sentence = temp.split(' ')
                    for token in sentence:
                        if token in self.single_word:
                            change = True
                            self.counts[token][dt_key] = self.counts[token].get(dt_key, 0) + 1

                    if change or travelflag:
                        outfile.write(json.dumps(tweet) + '\n')


        #print self.counts
        for key in self.counts:
            temp = self.counts[key]
            if temp != {}:
                df = p.DataFrame(list(temp.iteritems()), \
                columns=['Date', 'Count']).sort(columns=['Date'], ascending=False)
                city_formatted = str(key)
                df.to_csv('../pcounts/%s.csv'%(city_formatted.capitalize().replace('/', '')))


    def rebalance_counts(self):
        twitter_dir = '../twittercounts/'
        twitter_files = glob.glob('../twittercounts/*.csv')
        pcounts = glob.glob('../pcounts/*.csv')

        for i in pcounts:
            name = i.split('/')[1].replace('.csv','')
            for j in twitter_files:
                tname = j.split('/')[1].replace('.csv','')
                if name == tname:
                    # print 'Match for %s'%tname
                    data = p.read_csv(j)
                    new_data = p.read_csv(i)
                    if 'Datetime' in data:
                        data['Date'] = data.Datetime
                        del data['Datetime'], data['KeyWord']

                    data = data.append(new_data)
                    new = data.groupby(['Date'])
                    df = new.sum()
                    for i in range(0, 5):
                        try:
                            del df['Unnamed: %s'%str(i)]
                            del df['Unnamed: 0.%s'%str(i)]
                        except KeyError:
                            pass
                    df.to_csv(j)

if __name__ == '__main__':
    basepath2 = '/Volumes/Samsung/TwitterData'
    basepath = "/Volumes/Tweets/Data"
    a = TwitterExtractor(basepath2)
