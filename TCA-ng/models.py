import random
import cells

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
        if len(self.exit_routes) > 0:
            car.route = random.choice(self.exit_routes)
        else:
            car.route = None
    
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
    
    def get_view(self, desc=False):
        max_x = 0
        max_y = 0
        for cell in self.cells:
            max_x = max(max_x, cell.viewer_address[0] + 1)
            max_y = max(max_y, cell.viewer_address[1] + 1)

        grid = [[""]*max_x for _ in range(max_y)]

        for cell in self.cells:
            grid[cell.viewer_address[1]][cell.viewer_address[0]] = '.' if not cell.car else cell.car.speed
            if desc:
                grid[cell.viewer_address[1]][cell.viewer_address[0]] = cell.id
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
    
    def text_view(self, desc=False):
        grid = self.get_view(desc=desc)
        string = '\n'.join(''.join('%3s' % x for x in y) for y in grid)
        return string
    