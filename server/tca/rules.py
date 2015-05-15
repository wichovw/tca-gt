import random
import tca.cellaut as ca

class TCARule(ca.Rule):
    
    vmax = 5
    random_slow_p = 0.3
    background = 0

class StatesRule(TCARule):
    """Rules for calculating new state of non-empty cells"""
    
    def populate(self, map, address):
        self.state = map.get(address)
        self.front_gap = 0
        for cell in map.states(address, self.vmax)[0]:
            if cell == self.background:
                self.front_gap += 1
            else:
                break
        
    def apply(self):
        # if background, no calculations needed
        if self.state == self.background:
            return self.background
        
        vel, size, wagon = self.state
        
        # Nasch acceleration rule
        vel = min(vel + 1, self.vmax)
        
        # Nasch gap consideration rule
        vel = min(vel, self.front_gap)
        
        # Nasch randomly slowing of vehicle
        if random.random() < self.random_slow_p:
            vel = max(vel - 1, 0)
            
        return (vel, size, wagon)
    
class MovementRule(TCARule):
    """Rules for 'moving the cars' to their new positions"""
    
    def populate(self, map, address):
        self.state = map.get(address)
        self.back_gap = 0
        self.back_car = self.background
        for cell in map.states(address, self.vmax)[3]:
            if cell == self.background:
                self.back_gap += 1
            else:
                self.back_car = cell
                break

    def apply(self):
        # if car is stopped on cell
        if self.state != self.background and self.state[0] == 0:
                return self.state
        
        # if back car will land on cell
        if self.back_car != self.background and self.back_car != None:
            if self.back_car[0] == self.back_gap + 1:
                return self.back_car
            
        # return background otherwise
        return self.background