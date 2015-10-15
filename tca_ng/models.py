import random
import tca_ng.cells


class Automaton:
    topology = None
    generation = 0
    cycle = 40
    
    def get_cycle_time(self):
        return self.generation % self.cycle
    
    def update(self):
        for cell in self.topology.endpoint_cells:
            rule = cell.endpoint_rule_class(cell)
            rule.apply_()

        for cell in self.topology.cells:
            cell.rule = cell.rule_class(cell)

        for cell in self.topology.cells:
            cell.rule.pre_setting()
        for cell in self.topology.cells:
            cell.rule.apply_()
            
        for cell in self.topology.cells:
            cell.rule = cell.rule_class(cell)

        for cell in self.topology.cells:
            cell.rule.calculate()

        for cell in self.topology.cells:
            cell.rule.apply_()
            
        for semaphore in self.topology.semaphores:
            semaphore.update()
            
        self.generation += 1


class Street:
    id = 0
    cells = []
    exit_routes = []
    length = None
    lanes = None
    
    def __init__(self):
        self.id = Street.id
        Street.id += 1
        self.cells = []
        self.exit_routes = []
        
    def __repr__(self):
        return "<Street: %s>" % self.id
    
    def car_entry(self, car):
        if len(self.exit_routes) > 0:
            car.route = random.choice(self.exit_routes)
        else:
            car.route = None


class Route:
    id = 0
    cells = []
    entrance_lane = None
    
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

    # Eddy
    in_streets = []
    out_streets = []

    semaphore = None
    
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


class Semaphore:
    id = 0
    lights = []
    counter = 0
    active = 0
    schedule = None
    topology = None
    
    def __init__(self):
        self.id = Semaphore.id
        Semaphore.id += 1
        self.lights = []
        self.schedule = {}
        
    def __repr__(self):
        return "<Semaphore: %s>" % (self.id)
    
    def set_schedule(self, schedule):
        prev = None
        for period_start in sorted(schedule):
            light = schedule[period_start]
            self.schedule[period_start] = {
                'light': light,
                'change': 0,
            }
            if prev is not None:
                self.schedule[prev]['change'] = period_start
            prev = period_start
            
    def get_schedule(self):
        schedule = dict()
        for k, v in self.schedule.items():
            schedule[k] = v['light']
        return schedule
    
    def update(self):
        time = self.topology.automaton.get_cycle_time()
        change = self.schedule[self.active]['change']
        change = change if change != 0 else self.topology.automaton.cycle
        if time == 0:
            self.get_active_light().free = False
            self.active = 0
            self.get_active_light().free = True
        elif time >= change:
            self.get_active_light().free = False
            self.active = self.schedule[self.active]['change']
            self.get_active_light().free = True
    
    def get_active_light(self):
        return self.schedule[self.active]['light']


class Light:
    id = 0
    routes = []
    viewer_address = None
    semaphore = None
    free = False
    
    def __init__(self):
        self.id = Light.id
        Light.id += 1
        self.routes = []
        
    def __repr__(self):
        return "<Light: %s (%s)>" % (self.id, 1 if self.free else 0)


class Topology:
    cells = []
    endpoint_cells = []
    lights = []
    semaphores = []

    # Eddy
    intersections = []

    cars = []
    automaton = None
    
    def __init__(self):
        self.cells = []
        self.endpoint_cells = []
        self.lights = []
        self.semaphores = []
        self.cars = []
    
    def get_view(self, desc=False):
        max_x = 0
        max_y = 0
        for cell in self.cells:
            max_x = max(max_x, cell.viewer_address[0] + 1)
            max_y = max(max_y, cell.viewer_address[1] + 1)

        grid = [[""]*max_x for _ in range(max_y)]

        for light in self.lights:
            grid[light.viewer_address[1]][light.viewer_address[0]] = 'o' if light.free else 'x'
        
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
        
        for light in self.lights:
            x = light.viewer_address[0]
            y = light.viewer_address[1]
            color = -1
            if light.free:
                color = '00ff00'
            else:
                color = 'ff0000'
            grid[x][y] = color
        
        for cell in self.cells:
            x = cell.viewer_address[0]
            y = cell.viewer_address[1]
            color = -1
            if isinstance(cell, tca_ng.cells.EndpointEntranceCell):
                color = 'bb99bb'
            elif isinstance(cell, tca_ng.cells.EndpointExitCell):
                color = 'ffbb33'
            elif isinstance(cell, tca_ng.cells.IntersectionCell):
                color = 'dddddd'
            if cell.car is not None:
                color = '99cc99'
                if cell.car.id % 10 == 0:
                    color = '555599'
            grid[x][y] = color
                
        return grid
    
    def text_view(self, desc=False):
        grid = self.get_view(desc=desc)
        string = '\n'.join(''.join('%3s' % x for x in y) for y in grid)
        return string

