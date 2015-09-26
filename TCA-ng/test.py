import example_maps 
import random
import cells
import cars
import rules

if __name__ == "__main__":
    tca = example_maps.Automaton()
    topo = example_maps.simple_map()
#    topo = example_maps.simple_2_streets()
    tca.topology = topo
    print(topo.text_view())
    
    for cell in topo.cells:
        print(cell, cell.get_front_cells(3))
    
    for _ in range(10):
        tca.update()
        print(topo.text_view())