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
    
    for cell in topo.endpoint_cells:
        rule = cell.endpoint_rule_class(cell)
        rule.apply_()
    
    print(topo.text_view())
    
    for cell in topo.cells:
        cell.rule = cell.rule_class(cell)
        
    for cell in topo.cells:
        cell.rule.calculate()
        
    print(topo.text_view())
        
    for cell in topo.cells:
        cell.cell.rule.apply_()
        
    print(topo.text_view())