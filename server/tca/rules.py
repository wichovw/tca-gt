import random
import tca.cellaut as ca

class TCARule(ca.Rule):
    
    vmax = 1
    random_slow_p = 0.3
    background = 0
    change_lane_p = 0.5

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

        self.left_gap = 0
        self.right_gap = 0
        neighbors = map.neighbors(address)

        if neighbors[0] == self.background:
            self.left_gap += 1

        if neighbors[4] == self.background:
            self.right_gap += 1

    def apply(self):
        # if background, no calculations needed
        if self.state == self.background:
            return self.background
        
        car = self.state.clone()
        
        # Nasch acceleration rule
        car.speed = min(car.speed + 1, self.vmax)
        
        # Nasch gap consideration rule
        car.speed = min(car.speed, self.front_gap)
        
        # Nasch randomly slowing of vehicle
        if random.random() < self.random_slow_p:
            car.speed = max(car.speed - 1, 0)

        # TCA_GT changing lane intention
        if random.random() < self.change_lane_p:
            if self.left_gap == 0 and self.right_gap == 0:
                car.change_lane_intention = 0
            elif self.left_gap > 0:
                car.change_lane_intention = -1
            elif self.right_gap > 0:
                car.change_lane_intention = 1
            
        return car
    
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
        if self.state != self.background and self.state.speed == 0:
                return self.state
        
        # if back car will land on cell
        if self.back_car != self.background and self.back_car != None:
            if self.back_car.speed == self.back_gap + 1:
                return self.back_car
            
        # return background otherwise
        return self.background