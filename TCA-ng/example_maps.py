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
    exit_routes = []
    
    def __init__(self):
        self.id = Street.id
        Street.id += 1
        self.cells = []
        self.exit_routes = []
        
    def __repr__(self):
        return "<Street: %s>" % (self.id)
    
    def car_entry(self, car):
        car.route = random.choice(self.exit_routes)
    
class Route:
    id = 0
    cells = []
    
    def __init__(self):
        self.id = Route.id
        Route.id += 1
        self.cells = []
        
    def __repr__(self):
        return "<Route: %s>" % (self.id)
    
class Intersection:
    id = 0
    cells = []
    routes = []
    
    def __init__(self):
        self.id = Intersection.id
        Intersection.id += 1
        self.cells = []
        self.routes = []
        
    def __repr__(self):
        return "<Intersection: %s>" % (self.id)
    
    def get_valid_route(self, cell):
        for route in self.routes:
            if cell in route.cells:
                return route
        raise KeyError
    
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
#            grid[cell.viewer_address[1]][cell.viewer_address[0]] = cell.id
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

def simple_intersection(rate=0.8):
    topo = Topology()
    """
           v
         
           1
    >   0  4  2
           3
    """
    topo.cells = []
    topo.cells.append(cells.IntersectionEntranceCell())
    topo.cells.append(cells.IntersectionEntranceCell())
    topo.cells.append(cells.IntersectionExitCell())
    topo.cells.append(cells.IntersectionExitCell())
    topo.cells.append(cells.IntersectionCell())
    
    int_ = Intersection()
    
    routes = []
    int_.routes = routes
    routes.append(Route())
    routes.append(Route())
    routes.append(Route())
    routes.append(Route())
    
    routes[0].cells = [topo.cells[0], topo.cells[4], topo.cells[2]]
    routes[1].cells = [topo.cells[0], topo.cells[4], topo.cells[3]]
    routes[2].cells = [topo.cells[1], topo.cells[4], topo.cells[3]]
    routes[3].cells = [topo.cells[1], topo.cells[4], topo.cells[2]]
    
    topo.cells[0].viewer_address = [0, 1]
    topo.cells[0].intersection = int_
    topo.cells[0].routes = [routes[0], routes[1]]
    topo.cells[0].rate = rate
    
    topo.cells[1].viewer_address = [1, 0]
    topo.cells[1].intersection = int_
    topo.cells[1].routes = [routes[2], routes[3]]
    topo.cells[1].rate = rate
    
    topo.cells[2].viewer_address = [2, 1]
    topo.cells[2].intersection = int_
    topo.cells[2].routes = [routes[0], routes[3]]
    topo.cells[2].rate = rate
    
    topo.cells[3].viewer_address = [1, 2]
    topo.cells[3].intersection = int_
    topo.cells[3].routes = [routes[1], routes[2]]
    topo.cells[3].rate = rate
    
    topo.cells[4].viewer_address = [1, 1]
    topo.cells[4].intersection = int_
    topo.cells[4].routes = [routes[0], routes[1], routes[2], routes[3]]
    
    return topo
        
def simple_map(size=5):
    topo = Topology()
    
    streets = []
    streets.append(generate_street(size))
    streets.append(generate_street(size))
    streets.append(generate_street(size))
    streets.append(generate_street(size))
    
    int_ = simple_intersection()
    
    streets[0].cells[0].street.routes = int_.cells[0].routes
    streets[1].cells[0].street.routes = int_.cells[0].routes
    
    for cell in streets[0].cells:
        cell.viewer_address[1] += size + 1
    for cell in streets[2].cells:
        cell.viewer_address[0] += size + 3
        cell.viewer_address[1] += size + 1
        
    for cell in streets[1].cells:
        x = cell.viewer_address[0]
        cell.viewer_address[0] = size + 1
        cell.viewer_address[1] = x
    for cell in streets[3].cells:
        x = cell.viewer_address[0]
        cell.viewer_address[0] = size + 1
        cell.viewer_address[1] = x + size + 3
        
    for cell in int_.cells:
        cell.viewer_address[0] += size
        cell.viewer_address[1] += size
        
    streets[0].cells[-1].connection = int_.cells[0]
    streets[1].cells[-1].connection = int_.cells[1]
    streets[2].cells[0].connection = int_.cells[2]
    streets[3].cells[0].connection = int_.cells[3]
    
    int_.cells[0].connection = streets[0].cells[-1]
    int_.cells[1].connection = streets[1].cells[-1]
    int_.cells[2].connection = streets[2].cells[0]
    int_.cells[3].connection = streets[3].cells[0]
    
    streets[0].cells[-1].front_cell = int_.cells[0]
    streets[1].cells[-1].front_cell = int_.cells[1]
#    int_.cells[2].connection = streets[2].cells[0]
#    int_.cells[3].connection = streets[3].cells[0]
        
    for street in streets:
        topo.cells += street.cells
    topo.cells += int_.cells
    topo.endpoint_cells = [
        streets[0].cells[0],
        streets[1].cells[0],
        streets[2].cells[-1],
        streets[3].cells[-1],
    ]
        
    return topo
        
def simple_2_streets(size=5):
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