from tca_ng import example_maps
import random
from tca_ng import cells
from tca_ng import cars
from tca_ng import rules
from tca_ng import models
from tca_ng import map_parser
from viewer_ng import test as viewer
import json

def test():
#    tca = models.Automaton()
#    topo = example_maps.grid_2lane_map()
#    tca.topology = topo
#    topo.automaton = tca
#    
#    print(topo.text_view(desc=True))
    
#    for _ in range(100):
#        print(tca.generation, '-', tca.get_cycle_time())
#        tca.update()
#        print(topo.text_view())
#        print()
#            
#    print(topo.text_view(desc=True))
    
#    filename = 'simple_intersection'
#    
#    data = {}
#    with open('tca_ng/maps/%s.json' % filename) as f:
##        try:
#            data = json.loads(f.read())
##        except:
##            print("Something is wrong with topology object")
##            return
#    
##    topo = map_parser.parse(data)

#    topo1 = example_maps.grid_2lane_map(width=2, height=2)
#    print('map created')
#    data = map_parser.render(topo1)
#    data['topology']['name'] = 'grid16'
#    print('map saved')
#    with open('tca_ng/maps/%s.json' % data['topology']['name'], 'w') as outfile:
#        json.dump(data, outfile, sort_keys=True, indent=2)
#    topo2 = map_parser.parse(data)

    data = {}
    with open('tca/maps/%s.json' % 'grid16') as raw_file:
        data = json.load(raw_file)
    
    topo2 = map_parser.parse(data)
    
    print('map loaded')
    viewer.start_viewer(topo2)