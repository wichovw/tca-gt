from tca import parser, base, viewer
import json

def test(map_name, run_viewer=True):
    data = {}
    with open('tca/maps/%s.json' % map_name) as raw_file:
        data = json.load(raw_file)
    topo = parser.parse(data)
    print('map %s loaded' % data['topology']['name'])
    
    tca = base.Automaton(topo)
    viewer.start(tca)
    
if __name__ == '__main__':
    test('grid16')