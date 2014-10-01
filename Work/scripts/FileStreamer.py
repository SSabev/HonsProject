from twython import TwythonStreamer
import time
import datetime
import json
import sys

class MyStreamer(TwythonStreamer):

    def add_file_handler(self, filename):
        self.f = open(filename, 'a')
    
    def on_success(self, data):
        if 'text' in data:
            keys_wanted = ['text', 'id', 'source', 'coordinates', 'entities', 'id_str', 'retweet_count', 'favorited', 'geo', 'lang', 'filter_level', 'place', 'created_at']
            user_info_keys = ['id','geo_enabled', 'name', 'lang','screen_name', 'time_zone', 'friends_count']
            user_info = data['user']
            new_data = {key : data[key] for key in keys_wanted}
            new_data['user'] = {key: data['user'][key] for key in user_info_keys}
            if 'media' in new_data['entities'].keys():
                del new_data['entities']['media']
            self.f.write(json.dumps(new_data) + '\n')

    def on_error(self, status_code, data):
        print status_code, " going to sleep for 5 secs"
        time.sleep(20)

if __name__=='__main__':
    

    access_token_key = "43737143-h1HZ1gS8SkYUlH4jCM82D155MyvKlGo9vp7YCNE68"
    access_token_secret = "r7eR4IBl3054ezscp841Vs7a3cyRbfw8IafwSTyZI"

    consumer_key = "euU48zARDp9y3TGrWQVn23BeA"
    consumer_secret = "SKXP77rCNJSuwKekozDL1kMH9TlxjRtcfpc6m7rgTbvDIJcgy1"
    i = 0
    while True:
        if i == 0:
            filename = sys.argv[1]
            print filename
        else:
            filename = sys.argv[1].replace(filename[-2:], str(int(filename[-2:])+1) )
            
        stream = MyStreamer(consumer_key, consumer_secret,
                          access_token_key, access_token_secret)
        stream.add_file_handler(filename)
        try:
            stream.statuses.filter(track='twitter', locations='50.035974,-11.491699,58.83649,1.516113', language='en')
            stream.f.close()
        except:
            print "Something happenned and I don't care!"
