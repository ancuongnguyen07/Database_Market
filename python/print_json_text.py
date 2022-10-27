import json
import sys

JSON_PATH = r'../database/'

file_name = sys.argv[1]
try:
    with open(JSON_PATH + file_name, 'r') as fp:
        json_obj = json.load(fp)
        print(json_obj['text'])
except IOError as e:
    print(e)