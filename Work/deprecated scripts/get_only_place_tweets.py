from terms import terms, countries
import json
import glob

def get_cities():
    f = open('tbcities.dat', 'r')
    cities = {}
    for line in f:
        temp = line.split('\t')
        name = temp[1]
        cities[name] = ''
    return cities

if __name__ == '__main__':
    cities = get_cities()
    multi_word_cities = [i for i in cities if len(i.split(' ')) >= 2]
    multi_word_countries = [i for i in countries if len(i.split(' ')) >= 2]

    multi_word = multi_word_cities + multi_word_countries
    #one_word_cities = [i for i in cities if len(i.split(' ')) < 2]

    processed = ["/Volumes/Tweets/Data/%s"%i.split('/')[-1] for i in glob.glob('traveltweets_expanded/*')]
    print processed
    all_the_files = [i for i in glob.glob(r'/Volumes/Tweets/Data/data-dump-with-dt-*') if i not in processed]
    print all_the_files
    
    for i in all_the_files: 
        data_file = open(i, 'r')
        print "Processing %s"%i
        filename_current = i.split('/')[-1]
        outfile = open('traveltweets_expanded/%s'%filename_current, 'wb')
        t_flag = False
        p_flag = False
        mc_flag = False
        world_cup_flag = False
        for line in data_file:
            try:
                tweet = json.loads(line)
                temp = tweet['text'].encode('utf-8')
                wc = temp.lower()
                if 'brazil' in wc or 'world cup' in wc or 'rio de janerio' in wc or 'sao paolo' in wc:
                    world_cup_flag = True
                
                text = temp.split()
                
                for i in text:
                    if i in cities or i in countries:
                        p_flag = True
                    if i in terms:
                        t_flag = True

                for i in multi_word:
                    if i in wc:
                        p_flag = True

                if (p_flag and t_flag) or p_flag or world_cup_flag: 
                    outfile.write(json.dumps(tweet) + '\n')

                p_flag = False
                t_flag = False
                mc_flag = False
                world_cup_flag = False
            except ValueError:
                print line
        data_file.close()
        outfile.close()
        print "Finished %s"%i
