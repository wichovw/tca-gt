import example_maps 
import random
import cells
import cars
import rules

if __name__ == "__main__":
    tca = example_maps.Automaton()
    topo = example_maps.simple_map()
    tca.topology = topo
    print(topo.text_view())
    
    print(topo.cells[0].street.cells)
    print(topo.cells[5].street.cells)
    
    for cell in topo.cells:
        print(cell, cell.get_front_cells(3))
    
    for _ in range(10):
        tca.update()
        print(topo.text_view())