import random
import tca.cellaut as ca

class TCARule(ca.Rule):
    
    vmax = 1
    random_slow_p = 0.3
    background = 0
    change_lane_p = 0.2

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

        self.right_change_allowed = False
        self.left_change_allowed = False

        # verify if right cell is empty
        if map.states(address, 1)[1][0] == self.background:
            self.right_back_gap = 0
            self.right_car_speed = 0

            # verify if car speed < gap
            for cell in map.states(address, self.vmax)[2]:
                if cell == self.background:
                    self.right_back_gap += 1
                elif cell is None:
                    break
                else:
                    self.right_car_speed = cell.speed
                    break

            # Verify if car is allowed change
            if self.right_car_speed < self.right_back_gap:
                self.right_change_allowed = True


        # verify if left cell is empty
        if map.states(address, 1)[5][0] == self.background:
            self.left_back_gap = 0
            self.left_car_speed = 0

            # verify if car speed < gap
            for cell in map.states(address, self.vmax)[4]:
                if cell == self.background:
                    self.left_back_gap += 1
                elif cell is None:
                    break
                else:
                    self.left_car_speed = cell.speed
                    break

            # Verify if car is allowed change
            if self.left_car_speed < self.left_back_gap:
                self.left_change_allowed = True


    def apply(self):
        # if background, no calculations needed
        if self.state == self.background:
            return self.background

        self.state.change_lane_intention = 0

        car = self.state.clone()
        car.change_lane_intention = 0
        
        # Nasch acceleration rule
        car.speed = min(car.speed + 1, self.vmax)
        
        # Nasch gap consideration rule
        car.speed = min(car.speed, self.front_gap)
        
        # Nasch randomly slowing of vehicle
        if random.random() < self.random_slow_p:
            car.speed = max(car.speed - 1, 0)

        # TCA_GT changing lane intention
        if random.random() < self.change_lane_p:
            # Right allowed
            if self.right_change_allowed and not self.left_change_allowed:
                car.change_lane_intention = 1
            # Left allowed
            elif self.left_change_allowed and not self.right_change_allowed:
                car.change_lane_intention = -1
            # Both allowed
            elif self.right_change_allowed and self.left_change_allowed:
                if random.random() < 0.5:
                    car.change_lane_intention = 1
                else:
                    car.change_lane_intention = -1
            else:
                car.change_lane_intention = 0

            
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

        self.left_car = self.background
        self.right_car = self.background
        # verify right lane
        if map.states(address, 1)[1][0] != self.background and map.states(address, 1)[1][0] is not None:
            if map.states(address, 1)[1][0].change_lane_intention == -1:
                self.right_car = map.states(address, 1)[1][0]

        # verify left lane
        if map.states(address, 1)[5][0] != self.background and map.states(address, 1)[5][0] is not None:
            if map.states(address, 1)[5][0].change_lane_intention == 1:
                self.left_car = map.states(address, 1)[5][0]


    def apply(self):
        # if car is stopped on cell
        if self.state != self.background and self.state.speed == 0 and self.state.change_lane_intention == 0:
            return self.state

         # if lane change allowed
        if self.left_car != self.background and self.left_car is not None:
            return self.left_car

        if self.right_car != self.background and self.right_car is not None:
            return self.right_car
        
        # if back car will land on cell
        if self.back_car != self.background and self.back_car is not None:
            if self.back_car.speed == self.back_gap + 1 and self.back_car.change_lane_intention == 0:
                return self.back_car
            
        # return background otherwise
        return self.background