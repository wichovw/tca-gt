from example_maps import simple_street
import random
import cells
import cars
import rules

class Automaton:
    topology = None

if __name__ == "__main__":
    tca = Automaton()
    topo = simple_street()
    tca.topology = topo
    print(topo.text_view())
    
    # update
    # generation and consumption of cars
    
#    for cell in topo
    
#    for cell in topo.endpoint_cells:
#        if cell.rate < random.uniform(0, 1):
#            continue
#        if cell.type_ == cells.MAP_ENTRANCE_CELL:
#            if cell.car is not None:
#                continue
#            car = cars.Car()
#            car.cell = cell
#            cell.car = car
#            topo.cars.append(car)
#        if cell.type_ == cells.MAP_EXIT_CELL:
#            if cell.car is None:
#                continue
#            car = cell.car
#            cell.car = None
#            topo.cars.remove(car)
#    
#    print(topo.text_view())
#    
#    # calculate provisional
#    
#    for cell in topo.cells:
#        if cell.car is None:
#            continue
#        rule = rules.Rule(cell.car)
#        rule.calculate()
#    
#    # populate provisionals
#    
#    for cell in topo.cells:
#        cell.rule.apply_()
#        
#    print(topo.text_view())