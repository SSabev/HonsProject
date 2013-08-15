from twython import TwythonStreamer
import time
import datetime
import json
import sys

class MyStreamer(TwythonStreamer):

    def add_file_handler(self, filename):
        self.f = open(filename, 'wb')
    
    def on_success(self, data):
        if 'text' in data:
            keys_wanted = ['text', 'id', 'source', 'coordinates', 'entities', 'id_str', 'retweet_count', 'favorited', 'geo', 'lang', 'filter_level', 'place']
            user_info_keys = ['id','geo_enabled', 'name', 'lang','screen_name', 'time_zone', 'friends_count']
            user_info = data['user']
            new_data = {key : data[key] for key in keys_wanted}
            new_data['user'] = {key: data['user'][key] for key in user_info_keys}
            if 'media' in new_data['entities'].keys():
                del new_data['entities']['media']
            self.f.write(str(new_data) + '\n')

    def on_error(self, status_code, data):
        print status_code

if __name__=='__main__':
    filename = sys.argv[1]
    print filename

    access_token_key = "43737143-h1HZ1gS8SkYUlH4jCM82D155MyvKlGo9vp7YCNE68"
    access_token_secret = "r7eR4IBl3054ezscp841Vs7a3cyRbfw8IafwSTyZI"

    consumer_key = "khnoZ4PLfzPbvSIBYm6yg"
    consumer_secret = "oc4fsNCO1aWeVd9kyG1I7Cl8MsMuHVc1tHvK8dWnWJk"

    stream = MyStreamer(consumer_key, consumer_secret,
                      access_token_key, access_token_secret)
    stream.add_file_handler(filename)

    stream.statuses.filter(track='twitter', locations='50.035974,-11.491699,58.83649,1.516113', language='en')
    stream.f.close()