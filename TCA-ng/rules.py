import cells, cars
import random

class Rule:
    cell = None
    car = None
    
    def __init__(self, cell):
        self.cell = cell
        self.cell.p = cells.ProvisionalCell(self.cell)
        if cell.car is not None:
            self.car = cell.car
            self.car.p = cars.ProvisionalCar(self.car)
        self.populate()
        
    def populate(self):
        raise NotImplementedError
        
    def calculate(self):
        raise NotImplementedError
        
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
    
    def populate(self):
        self.generate = False
        if self.cell.connection is not None:
            return
        if self.car is not None:
            return
        if random.random() <= self.cell.rate:
            self.generate = True
            
    def apply_(self):
        if self.generate:
            car = cars.Car()
            car.cell = self.cell
            car.speed = self.cell.speed
            self.cell.car = car
    
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
            self.cell.car = None
            self.car.cell = None