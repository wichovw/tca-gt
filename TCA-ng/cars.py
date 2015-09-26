
class ProvisionalCar:
    speed = 0
    cell = None
    
    def __init__(self, car):
        self.speed = car.speed
        self.cell = car.cell

class Car:
    id = 0
    cell = None
    speed = 0
    route = None
    v_max = 3
    p = None
    
    decelerate_rate = 0.3
    
    def __init__(self):
        self.id = Car.id
        Car.id += 1
    
    def __repr__(self):
        return "<Car: %s (%s)>" % (self.id, self.speed)
    
    def apply_rules(self):
        self.speed = self.p.speed
        self.cell = self.p.cell
    