import cellaut as ca
from tca.rules import StatesRule, MovementRule

class TCAAutomaton(ca.Automaton):
    
    speed_rule = ca.StatesRule
    move_rule = ca.MovementRule
    
    def __init__(self, map):
        Automaton.__init__(self, map)
        self.workmap = map.clone()
        
    def update(self):
        self.update_step(speed_rule)
        self.swap()
        self.update_step(move_rule)
        self.swap()
        Automaton.update(self)
        
    def update_step(self, rule_class):
        for street_id in self.map.streets:
            street = self.map.streets[street_id]
            for lane in range(street.width):
                for cell in range(street.length):
                    address = street_id
                    rule = rule_class(self.map, address)
                    value = rule.apply()
                    self.workmap.set(address, value)
                    
    def swap(self):
        self.map.buffer = self.workmap.buffer