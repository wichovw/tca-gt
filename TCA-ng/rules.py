import cells, cars
import random

class Provisional:
    def __init__(self, obj):
        if isinstance(obj, cells.Cell):
            self.car = obj.car
        elif isinstance(obj, cars.Car):
            self.speed = obj.speed

class Rule:
    max_speed = 3
    rand = 0.3
    
    def __init__(self, car):
        self.car = car
        self.cell = cell
        car.p = Provisional(car)
        cell.p = Provisional(cell)
        self.populate()
        
    def populate(self):
        self.front_gap = 0
        for cell in self.cell.front_cells:
            if cell.car is not None:
                break
            self.front_gap += 1
    
    def nasch_rules(self):
        # rule 1 
        self.car.p.speed = min(self.car.p.speed + 1, self.max_speed)
        # rule 2
        self.car.p.speed = min(self.car.p.speed, self.front_gap)
        # rule 3
        if random.uniform(0, 1) < self.rand:
            self.car.p.speed = max(0, self.car.p.speed - 1)