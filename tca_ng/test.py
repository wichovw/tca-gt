from tca_ng import example_maps
import random
from tca_ng import cells
from tca_ng import cars
from tca_ng import rules
from tca_ng import models

def test():
    tca = models.Automaton()
    topo = example_maps.grid_2lane_map()
    tca.topology = topo
    topo.automaton = tca
    
    print(topo.text_view(desc=True))
    
#    for _ in range(100):
#        print(tca.generation, '-', tca.get_cycle_time())
#        tca.update()
#        print(topo.text_view())
#        print()
#            
#    print(topo.text_view(desc=True))
    