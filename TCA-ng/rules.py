import cells, cars
import random

class Rule:
    cell = None
    car = None
    front_gap = 0
    front_cells = []
    
    def __init__(self, cell):
        self.cell = cell
        self.cell.p = cells.ProvisionalCell(self.cell)
        if cell.car is not None:
            self.car = cell.car
            self.car.p = cars.ProvisionalCar(self.car)
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
    pass
    
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
        if isinstance(self.cell, cells.StreetCell):
            self.is_street = True
            
    def apply_(self):
        if self.generate:
            car = cars.Car()
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