import re
import json

def trim_file(infile, outfile):
	for line in infile:
	    line = line.replace(chr(0), '')
	    #line = re.sub('([{,])([^{:\s"]*):', lambda m: '%s"%s":'%(m.group(1),m.group(2)),line)
	    print line
	    data = json.loads(line)
	    if 'text' in data:
	        keys_wanted = ['text', 'id', 'source', 'coordinates', 'entities', 'id_str', 'retweet_count', 'favorited', 'geo', 'lang', 'filter_level', 'place']
	        user_info_keys = ['id','geo_enabled', 'name', 'lang','screen_name', 'time_zone', 'friends_count']
	        user_info = data['user']
	        new_data = {key : data[key] for key in keys_wanted}
	        new_data['user'] = {key: data['user'][key] for key in user_info_keys}
	        if 'media' in new_data['entities'].keys():
	            del new_data['entities']['media']
	        outfile.write(new_data)

def cleanup_file(infile, outfile):
	for line in infile:
	    line = line.replace(chr(0), '')
	    #line = re.sub('([{,])([^{:\s"]*):', lambda m: '%s"%s":'%(m.group(1),m.group(2)),line)
	    outfile.write(line)