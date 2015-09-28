import example_maps 
import random
import cells
import cars
import rules
import models

if __name__ == "__main__":
    tca = models.Automaton()
    topo = example_maps.simple_map()
#    topo = example_maps.simple_2_streets()
    tca.topology = topo
    print(topo.text_view())
    
    for cell in topo.cells:
        print(cell, cell.get_front_cells(3))
    
    for _ in range(10):
        tca.update()
        print(topo.text_view())
        
    s = set()
    cars = []
    for cell in topo.cells:
        if isinstance(cell, cells.StreetCell):
            s.add(cell.street)
        if cell.car:
            cars.append(cell.car)
            
    print(topo.text_view(desc=True))
            
    for car in sorted(cars, key=lambda x: x.cell.id):
        print(car.cell, car.route)