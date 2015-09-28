import example_maps 
import random
import cells
import cars
import rules
import models

if __name__ == "__main__":
    tca = models.Automaton()
    topo = example_maps.totito_map()
    tca.topology = topo
    
    print(topo.text_view(desc=True))
    
    for _ in range(1000):
        tca.update()
        print(topo.text_view())
            
    print(topo.text_view(desc=True))