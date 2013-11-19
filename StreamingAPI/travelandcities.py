from terms import terms
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

    current = ''
    all_the_files = [i for i in glob.glob(r'data-dump-with-dt-*') if i!=current]

    for i in all_the_files: 
        data_file = open(i, 'r')
        outfile = open('traveltweets/%s'%i, 'wb')
        t_flag = False
        p_flag = False
        for line in data_file:
            tweet = json.loads(line)
            text = tweet['text'].encode('utf-8').split()
            for i in text:
                if i in cities:
                    p_flag = True
                if i in terms:
                    t_flag = True
            if p_flag and t_flag:
                outfile.write(json.dumps(tweet) + '\n')
            p_flag = False
            t_flag = False
        data_file.close()
        outfile.close()
