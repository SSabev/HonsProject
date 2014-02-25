from dateutil.relativedelta import relativedelta
import glob
import pandas as p
import datetime as dt

    
def join_files(city,filenames):
    s_file, t_file = filenames
    searches = p.read_csv(s_file)
    tweets = p.read_csv(t_file)

    def conversion(date):
        try:
            temp = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except:
            temp = dt.datetime.strptime(date, '%Y-%m-%d')
        #temp = temp + relativedelta(days = 1)
        return temp.strftime('%Y-%m-%d')
    #print searches[0:2]
    #print tweets[0:2]a
    
    searches.Date = searches.Date.apply(conversion)
    tweets.Date = tweets.Date.apply(conversion)
    searches_and_tweets = searches.merge(tweets, on='Date', how='outer')

    try:
        searches_and_tweets['NSearches'] = searches_and_tweets['Searches']/float(max(searches_and_tweets['Searches']))
        searches_and_tweets.to_csv('tidydata/joined/%s.csv'%city)
    except ValueError:
        print "Something went wrong"

def tidy_up():
    tweet_files = glob.glob(r'tidydata/twitter/*.csv')
    ss_files = glob.glob(r'tidydata/se/*.csv')
    
    city_dict = {}
    for i in ss_files:
        city_name = i.replace('.csv','').split('/')[-1]
        tweet_file = None
        for j in tweet_files:
            other_name = j.replace('.csv','').split('/')[-1]
            if city_name == other_name:
                city_dict[city_name] = (i,j)


    tweets_files_names = [i.replace('.csv', '').split('/')[-1] for i in tweet_files]
    ss_files_names = [i.replace('.csv', '').split('/')[-1] for i in ss_files]
    
    print "Unmatched: "
    print set(tweets_files_names).difference(set(ss_files_names))
    return city_dict

if __name__ == '__main__':
    city_dict = tidy_up()

    for i in city_dict:
        print "Place is %s. SS file is %s, twitter file is %s"%(i, city_dict[i][0], city_dict[i][1])
        join_files(i, city_dict[i])

    print len(city_dict)

