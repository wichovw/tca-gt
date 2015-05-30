import copy
import tca.cellaut as ca
from tca.rules import StatesRule, MovementRule

class TCAAutomaton(ca.Automaton):
    
    speed_rule = StatesRule
    move_rule = MovementRule
    
    def __init__(self, map):
        super().__init__(map)
        self.workmap = map.clone()
        
    def update(self):
        self.update_step(self.speed_rule)
        self.swap()
        self.update_step(self.move_rule)
        self.swap()
        ca.Automaton.update(self)
        
    def update_step(self, rule_class):
        for street_id in self.map.streets:
            street = self.map.streets[street_id]
            for lane in range(street.width):
                for cell in range(street.height + street.front_offset):
                    address = (street_id, lane, cell)
                    rule = rule_class(self.map, address)
                    value = rule.apply()
                    self.workmap.set(address, value)
                    
    def swap(self):
        for street in self.map.streets:
            self.map.streets[street].buffer = copy.deepcopy(self.workmap.streets[street].buffer)