import rules

class ProvisionalCell:
    car = None
    
    def __init__(self, cell):
        self.car = cell.car

class Cell:
    id = 0
    car = None
    viewer_address = None
    rule = None
    rule_class = None
    p = None
    
    def __init__(self):
        self.id = Cell.id
        Cell.id += 1
    
    def __repr__(self):
        return "<Cell: %s>" % self.id
    
    def apply_rules():
        cell.car = cell.p.car
    
class StreetCell(Cell):
    rule_class = rules.StreetRule
    street = None
    lane = None
    cell = None
    cells_to_end = None
    front_cell = None
    
class IntersectionCell(Cell):
    rule_class = rules.IntersectionRule
    routes = None
    indexes = None
    
class EndpointCell(Cell):
    rate = 0
    connection = None
    
class EndpointEntranceCell(EndpointCell):
    endpoint_rule_class = rules.EntranceRule
    speed = 1
    
class EndpointExitCell(EndpointCell):
    endpoint_rule_class = rules.ExitRule
    
class StreetEntranceCell(EndpointEntranceCell, StreetCell):
    pass
    
class StreetExitCell(EndpointExitCell, StreetCell):
    pass

class IntersectionEntranceCell(EndpointEntranceCell, IntersectionCell):
    pass

class IntersectionExitCell(EndpointExitCell, IntersectionCell):
    pass