import json

def parse(map):
    with open('server/maps/%s.json' % map) as data_file:    
        data = json.load(data_file)
    return data