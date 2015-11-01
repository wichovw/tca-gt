import tca_ng.cells, tca_ng.cars
import random


class Rule:
    cell = None
    car = None
    front_gap = 0
    front_cells = []
    
    def __init__(self, cell):
        self.cell = cell
        self.cell.p = tca_ng.cells.ProvisionalCell(self.cell)
        if cell.car is not None:
            self.car = cell.car
            self.car.p = tca_ng.cars.ProvisionalCar(self.car)
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
            self.car.waits_for_lane_change = 0
            return
            
        dif = self.cell.lane - self.car.route.entrance_lane
        if dif != 0:
            if self.cell.cells_to_end <= 1 and self.car.route in self.cell.connection.intersection.semaphore.get_active_light().routes:
                self.car.waits_for_lane_change += 1
                if self.car.waits_for_lane_change >= self.car.changing_route_max_wait:
                    self.car.route = random.choice(self.cell.connection.routes)
                    self.car.waits_for_lane_change = 0
#                    self.cell.topology.foo_cells.append(self.cell)
#                    print('deadlock avoidance', self.cell.connection.intersection.id)
                
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
        if isinstance(self.cell, tca_ng.cells.StreetCell):
            self.is_street = True
            
    def apply_(self):
        if self.generate:
            car = tca_ng.cars.Car()
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
