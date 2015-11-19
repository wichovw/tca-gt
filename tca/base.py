"""
10/2015
Luis Valdeavellano - 11218
Universidad del Valle de Guatemala

Implementation of a Traffic Cellular Automata simulator
"""

import random

class Cell:
    id = 0
    car = None
    viewer_address = None
    rule = None
    rule_class = None
    p = None
    topology = None
    
    def __init__(self):
        self.id = Cell.id
        Cell.id += 1
    
    def __repr__(self):
        return "<Cell: %s (%s)>" % (self.id, '.' if self.car is None else self.car.speed)
    
    def apply_rules(self):
        self.car = self.p.car

class ProvisionalCell:
    car = None
    recipient = False
    
    def __init__(self, cell):
        self.car = cell.car

class ProvisionalCar:
    speed = 0
    cell = None
    
    def __init__(self, car):
        self.speed = car.speed
        self.cell = car.cell

class Rule:
    cell = None
    car = None
    front_gap = 0
    front_cells = []
    
    def __init__(self, cell):
        self.cell = cell
        self.cell.p = ProvisionalCell(self.cell)
        if cell.car is not None:
            self.car = cell.car
            self.car.p = ProvisionalCar(self.car)
        self.populate()
    
    def populate(self):
        if self.car is None:
            return
        self.front_gap = 0
        self.front_cells = self.cell.get_front_cells(self.car.v_max, self.car.route)
        for cell in self.front_cells:
            if cell.car is not None:
                break
            self.front_gap += 1
        
    def pre_setting(self):
        pass
        
    def calculate(self):
        if self.car is None:
            return
        self.nasch_rules()
        
    def nasch_rules(self):
        # rule 1 (acceleration):
        self.car.p.speed = min(self.car.p.speed + 1, self.car.v_max)
        
        # rule 2 (collide avoidance)
        self.car.p.speed = min(self.car.p.speed, self.front_gap)
        
        # rule 3 (stochastic deceleration)
        if random.random() < self.car.decelerate_rate:
            self.car.p.speed = max(0, self.car.p.speed - 1)
            
        # move car
        if self.car.p.speed > 0:
            self.car.p.cell = self.front_cells[self.car.p.speed - 1]
            self.car.p.cell.p.car = self.car
            self.car.p.cell.p.recipient = True
            if not self.cell.p.recipient:
                self.cell.p.car = None
        
    def apply_(self):
        self.cell.apply_rules()
        if self.car is not None:
            self.car.apply_rules()

class StreetRule(Rule):
    
    def pre_setting(self):
        super().pre_setting()
        self.calculate_changing_lane_rates()
        self.change_lane_rules()
        
    def calculate_changing_lane_rates(self):
        if self.car is None:
            return
        base = self.car.base_lane_changing_rate
        if self.car.route is None:
            self.car.right_change_rate = 0.5
            self.car.lane_changing_rate = base
            return
            
        dif = self.cell.lane - self.car.route.entrance_lane
        if dif != 0:
            if self.cell.cells_to_end <= 1:
                self.car.waits_for_lane_change += 1
                if self.car.waits_for_lane_change >= self.car.changing_route_max_wait:
                    self.car.route = random.choice(self.cell.connection.routes)
                    self.car.waits_for_lane_change = 0
#                    print('deadlock avoidance')
                
            self.car.right_change_rate = 1 if dif < 0 else 0
            self.car.lane_changing_rate = (self.cell.cell / self.cell.street.length) * (1 - base) + base
        else:
            self.car.right_change_rate = 0.5
            self.car.lane_changing_rate = (self.cell.cells_to_end / self.cell.street.length) * base
            self.car.waits_for_lane_change = 0
        
        
    def change_lane_rules(self):
        if self.car is None or random.random() > self.car.lane_changing_rate:
            return
        side = 'right' if random.random() < self.car.right_change_rate else 'left'
        dest_cell = getattr(self.cell, '%s_cell' % side)
        if dest_cell is not None and dest_cell.car is None:
            if not dest_cell.p.recipient:
                self.car.p.cell = dest_cell
                dest_cell.p.car = self.car
                dest_cell.p.recipient = True
                if not self.cell.p.recipient:
                    self.cell.p.car = None

class IntersectionRule(Rule):
    pass

class StreetCell(Cell):
    rule_class = StreetRule
    street = None
    lane = None
    cell = None
    cells_to_end = None
    front_cell = None
    right_cell = None
    left_cell = None
    
    def get_front_cells(self, n, route=None):
        cells = self.street.cells[self.lane][self.cell + 1 :]
        dif = n - len(cells)
        if dif > 0 and cells[-1].connection is not None:
            cells += cells[-1].get_front_cells(dif, route)
        return cells[:n]


class IntersectionCell(Cell):
    rule_class = IntersectionRule
    routes = None
    intersection = None
    
    def __init__(self):
        super().__init__()
        self.routes = []
        
    def get_front_cells(self, n, route=None):
        if route is None:
            return []
        cells = route.cells[route.cells.index(self) + 1 :]
        dif = n - len(cells)
        if dif > 0 and cells[-1].connection is not None:
            cells += cells[-1].get_front_cells(dif, route)
        return cells[:n]


class Car:
    id = 0
    cell = None
    speed = 0
    route = None
    v_max = 3
    p = None
    
    decelerate_rate = 0.3
    # Que tan agresivo es el carro para cambiar de carriles
    base_lane_changing_rate = 0.2
    # Que tan agresivo es en este momento el carro para cambiar de carril
    lane_changing_rate = 0.2
    # Que tan probable es que cambie a la derecha. Complemento a la izquierda
    right_change_rate = 0.5
    # Cuantas iteraciones esperaria al final de una calle para cambiar de carril
    # antes de cambiar de ruta
    changing_route_max_wait = 10
    # Cuantas iteraciones lleva esperando al final de una calle tratando de cambiar de carril
    waits_for_lane_change = 0
    
    def __init__(self):
        self.id = Car.id
        Car.id += 1
    
    def __repr__(self):
        return "<Car: %s (%s)>" % (self.id, self.speed)
    
    def apply_rules(self):
        if isinstance(self.p.cell, StreetCell):
            if not isinstance(self.cell, StreetCell) or (
                self.cell.street != self.p.cell.street
            ):
                    self.p.cell.street.car_entry(self)
        self.speed = self.p.speed
        self.cell = self.p.cell
        
        
class EntranceRule(Rule):
    generate = False
    is_street = False
    
    def populate(self):
        self.generate = False
        if self.cell.connection is not None:
            return
        if self.car is not None:
            return
        if random.random() <= self.cell.rate:
            self.generate = True
        if isinstance(self.cell, StreetCell):
            self.is_street = True
            
    def apply_(self):
        if self.generate:
            car = Car()
            car.cell = self.cell
            car.speed = self.cell.speed
            self.cell.car = car
            if self.is_street:
                self.cell.street.car_entry(car)
            self.cell.topology.cars.append(car)

class ExitRule(Rule):
    consume = False
    
    def populate(self):
        self.consume = False
        if self.cell.connection is not None:
            return
        if self.car is None:
            return
        if random.random() <= self.cell.rate:
            self.consume = True
            
    def apply_(self):
        if self.consume:
            self.cell.topology.cars.remove(self.car)
            self.cell.car = None
            self.car.cell = None

class EndpointCell(Cell):
    rate = 0
    connection = None

class EndpointEntranceCell(EndpointCell):
    endpoint_rule_class = EntranceRule
    speed = 1

class EndpointExitCell(EndpointCell):
    endpoint_rule_class = ExitRule
    
    def get_front_cells(self, n, route=None):
        if self.connection is None:
            return []
        elif isinstance(self.connection, StreetCell):
            return [self.connection] + self.connection.get_front_cells(n - 1, route)
        elif isinstance(self.connection, IntersectionCell):
            if (route in self.connection.intersection.semaphore.get_active_light().routes
                and route in self.connection.routes):
                return [self.connection] + self.connection.get_front_cells(n - 1, route)
            else:
                return []
        else:
            raise NotImplementedError


class StreetEntranceCell(EndpointEntranceCell, StreetCell):
    pass

class StreetExitCell(EndpointExitCell, StreetCell):
    pass

class IntersectionEntranceCell(EndpointEntranceCell, IntersectionCell):
    pass

class IntersectionExitCell(EndpointExitCell, IntersectionCell):
    pass

class Automaton:
    topology = None
    generation = 0
    cycle = 40
    
    def __init__(self, topology):
        self.topology = topology
        topology.automaton = self
    
    def get_cycle_time(self):
        return self.generation % self.cycle
    
    def sync_update(self, func):
        # Instantiation & population of rules
        for cell in self.topology.cells:
            cell.rule = cell.rule_class(cell)

        # Calculation of new values
        for cell in self.topology.cells:
            func(cell)
            
        # Syncronous application of new values
        for cell in self.topology.cells:
            cell.rule.apply_()
    
    def update(self):
        # Generation and consumption of cars
        for cell in self.topology.endpoint_cells:
            rule = cell.endpoint_rule_class(cell)
            rule.apply_()

        # Configuration changes on map 
        self.sync_update(lambda x: x.rule.pre_setting())
        
        # Cars movement rules application
        self.sync_update(lambda x: x.rule.calculate())
            
        # Update of semaphores states
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

    in_streets = []
    out_streets = []
    neighbors = []

    semaphore = None

    def __init__(self):
        self.id = Intersection.id
        Intersection.id += 1
        self.cells = []
        self.routes = []

        self.in_streets = []
        self.out_streets = []
        self.neighbors = []
        
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
        self.active = 0
        cycle_time = 0
        if len(self.schedule) > 0:
            self.get_active_light().free = False
            cycle_time = self.topology.automaton.get_cycle_time()
        self.schedule = {}
        for period_start in sorted(schedule):
            light = schedule[period_start]
            self.schedule[period_start] = {
                'light': light,
                'change': 0,
            }
            if period_start <= cycle_time:
                self.active = period_start
            if prev is not None:
                self.schedule[prev]['change'] = period_start
            prev = period_start
        self.get_active_light().free = True
        
            
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

    intersections = []
    streets = []

    cars = []
    automaton = None
    
    def __init__(self):
        self.cells = []
        self.endpoint_cells = []
        self.lights = []
        self.semaphores = []
        self.cars = []