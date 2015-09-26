import rules

class Cell:
    id = 0
    car = None
    viewer_address = None
    rule = None
    
    def __init__(self):
        self.id = Cell.id
        Cell.id += 1
    
    def __repr__(self):
        return "<Cell: %s>" % self.id
    
class StreetCell(Cell):
    rule = rules.StreetRule
    street = None
    lane = None
    cell = None
    cells_to_end = None
    front_cell = None
    
class IntersectionCell(Cell):
    rule = rules.IntersectionRule
    routes = None
    indexes = None
    
class EndpointCell(Cell):
    rate = 0
    connection = None
    
class EndpointEntranceCell(EndpointCell):
    rule = rules.EntranceRule
    
class EndpointExitCell(EndpointCell):
    rule = rules.ExitRule
    
class StreetEntranceCell(EndpointEntranceCell, StreetCell):
    pass
    
class StreetExitCell(EndpointExitCell, StreetCell):
    pass

class IntersectionEntranceCell(EndpointEntranceCell, IntersectionCell):
    pass

class IntersectionExitCell(EndpointExitCell, IntersectionCell):
    pass