from example_maps import simple_street
import random
import cells
import cars
import rules

class Automaton:
    topology = None
    
    def update(self):
        for cell in self.topology.endpoint_cells:
            rule = cell.endpoint_rule_class(cell)
            rule.apply_()

        for cell in self.topology.cells:
            cell.rule = cell.rule_class(cell)

        for cell in self.topology.cells:
            cell.rule.calculate()

        for cell in self.topology.cells:
            cell.rule.apply_()

if __name__ == "__main__":
    tca = Automaton()
    topo = simple_street()
    tca.topology = topo
    print(topo.text_view())
    
    for _ in range(10):
        tca.update()
        print(topo.text_view())