import copy
import tca.cellaut as ca
from tca.rules import StatesRule, MovementRule

class TCAAutomaton(ca.Automaton):
    
    speed_rule = StatesRule
    move_rule = MovementRule
    
    def __init__(self, map):
        super().__init__(map)
        self.workmap = map.clone()
        self.visited_map = map.clone()
        for street_id, street in self.visited_map.streets.items():
            for lane in range(street.width):
                for cell in range(street.height + street.front_offset):
                    self.visited_map.set((street_id, lane, cell), False)
        
    def update(self):
        self.update_step(self.speed_rule)
        self.swap()
        print(self.map.__str__(True))
        self.update_step(self.move_rule)
        self.swap()
        ca.Automaton.update(self)
        print(str(self.map))
        
    def update_step(self, rule_class):
        for street_id in self.map.streets:
            street = self.map.streets[street_id]
            for lane in range(street.width):
                for cell in range(street.height + street.front_offset):
                    address = (street_id, lane, cell)
                    rule = rule_class(self.map, address)
                    value = rule.apply()
                    if self.visited_map.get(address) and not value:
                        continue
                    self.workmap.set(address, value)
                    self.visited_map.set(address, True)
                    
    def swap(self):
        for street in self.map.streets:
            self.map.streets[street].buffer = copy.deepcopy(self.workmap.streets[street].buffer)
            self.map.streets[street].intersection.buffer = copy.deepcopy(self.workmap.streets[street].intersection.buffer)
            
        for street_id, street in self.visited_map.streets.items():
            for lane in range(street.width):
                for cell in range(street.height + street.front_offset):
                    self.visited_map.set((street_id, lane, cell), False)