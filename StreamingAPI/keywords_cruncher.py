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
                print dt_stamp
                break
                for hashtag in hastags:
                    text = hashtag['text']
                    self.hashtags[text] = self.hashtags.get(text, 0)
                    self.hashtags[text] +=1

    def dump_tags(self):

        print self.hashtags


if __name__ == '__main__':

    tags = KeyStats('data-dump-with-dt-19')

    # tags.dump_tags()
    delta = datetime.datetime.now() - tags.starttime
    
    outfile = open('outfile', 'wb')


    outfile.write(json.dumps(tags.hashtags, indent=4))
    outfile.write(json.dumps(sorted(tags.hashtags.items(), key=lambda x: x[1]), indent=4))
    outfile.close()

    print delta.seconds 
