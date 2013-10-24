import re
import json
import datetime 

class KeyStats(object):
    
    def __init__(self, filename):

        self.filehandler = open(filename, 'rb')
        self.starttime = datetime.datetime.now()
        self.hashtags = {}
        self.get_keywords()
        # self.something_else
    
    def get_keywords(self):
        for line in self.filehandler:
            data = json.loads(line)
            if 'entities' in data:
                hastags = data['entities']['hashtags']
                dt_stamp = datetime.datetime.strptime(data['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

                dt_key = dt_stamp.strftime('%Y-%m-%d %H')
                for hashtag in hastags:
                    text = hashtag['text']
                    if text not in self.hashtags:
                        self.hashtags[text] = {}
                        self.hashtags[text][key] = self.hashtags[text].get(dt_key, 0) + 1
                    else:
                        self.hashtags[text][key] = self.hashtags[text].get(dt_key, 0) + 1

    def dump_tags(self):

        print self.hashtags


if __name__ == '__main__':

    tags = KeyStats('data-dump-with-dt-19')

    # tags.dump_tags()
    delta = datetime.datetime.now() - tags.starttime
    
    outfile = open('outfile', 'wb')


    outfile.write(json.dumps(sorted(tags.hashtags.items(), key=lambda x: len(x[1]), reverse=True), indent=4))
    outfile.close()

    print delta.seconds 
