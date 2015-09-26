import cells
import random

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
            
class Street:
    id = 0
    cells = []
    
    def __init__(self):
        self.id = Street.id
        Street.id += 1
        self.cells = []
        
    def __repr__(self):
        return "<Street: %s>" % (self.id)
    
class Topology:
    cells = []
    endpoint_cells = []
    
    def __init__(self):
        self.cells = []
        self.endpoint_cells = []
    
    def get_view(self):
        max_x = 0
        max_y = 0
        for cell in self.cells:
            max_x = max(max_x, cell.viewer_address[0] + 1)
            max_y = max(max_y, cell.viewer_address[1] + 1)

        grid = [[""]*max_x for _ in range(max_y)]

        for cell in self.cells:
            grid[cell.viewer_address[1]][cell.viewer_address[0]] = '.' if not cell.car else cell.car.speed
        return grid
    
    def json_view(self):
        max_x = 0
        max_y = 0
        for cell in self.cells:
            max_x = max(max_x, cell.viewer_address[0] + 1)
            max_y = max(max_y, cell.viewer_address[1] + 1)
            
        grid = [[-2]*max_y for _ in range(max_x)]
        
        for cell in self.cells:
            x = cell.viewer_address[0]
            y = cell.viewer_address[1]
            color = -1
            if isinstance(cell, cells.EndpointEntranceCell):
                color = 'bb99bb'
            elif isinstance(cell, cells.EndpointExitCell):
                color = 'ffbb33'
            elif isinstance(cell, cells.IntersectionCell):
                color = 'dddddd'
            if cell.car is not None:
                color = '99cc99'
            grid[x][y] = color
                
        return grid
    
    def text_view(self):
        grid = self.get_view()
        string = '\n'.join(''.join('%3s' % x for x in y) for y in grid)
        return string
    

def generate_street(length, rate=0.8):
    topo = Topology()
    
    # cells declaration
    entrance = cells.StreetEntranceCell()
    topo.cells.append(entrance)
    topo.endpoint_cells.append(entrance)
    for _ in range(length - 2):
        topo.cells.append(cells.StreetCell())
    exit = cells.StreetExitCell()
    topo.cells.append(exit)
    topo.endpoint_cells.append(exit)
    
    street = Street()
    street.cells.append([])
        
    for i, cell in enumerate(topo.cells):
        street.cells[0].append(cell)
        cell.viewer_address = [i, 0]
        cell.street = street
        cell.lane = 0
        cell.cell = i
        cell.cells_to_end = length - i
        if i + 1 < len(topo.cells):
            cells.front_cell = topo.cells[i + 1]
        if isinstance(cell, cells.EndpointCell):
            cell.rate = rate
            
    return topo
        
def simple_map(size=5):
    topo = Topology()
    
    street1 = generate_street(size)
    street2 = generate_street(size)
    
    for cell in street2.cells:
        cell.viewer_address[0] += size
    
    exit = street1.cells[size - 1]
    entrance = street2.cells[0]
    
    exit.connection = entrance
    entrance.connection = exit
    
    exit.front_cell = entrance
    
    topo.cells = street1.cells + street2.cells
    topo.endpoint_cells = [street1.cells[0], street2.cells[size - 1]]
    return topo