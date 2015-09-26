import rules

class ProvisionalCell:
    car = None
    recipient = False
    
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
        return "<Cell: %s (%s)>" % (self.id, '.' if self.car is None else self.car.speed)
    
    def apply_rules(self):
        self.car = self.p.car
    
class StreetCell(Cell):
    rule_class = rules.StreetRule
    street = None
    lane = None
    cell = None
    cells_to_end = None
    front_cell = None
    
    def get_front_cells(self, n):
        cells = self.street.cells[self.lane][self.cell + 1 :]
        dif = n - len(cells)
        if dif > 0 and cells[-1].connection is not None:
            cells += cells[-1].get_front_cells(dif)
        return cells[:n]
    
class IntersectionCell(Cell):
    rule_class = rules.IntersectionRule
    routes = None
    intersection = None
    
    def get_front_cells(self, n, route=None):
        if route is None:
            route = self.intersection.get_valid_route(self)
        cells = route.cells[route.cells.index(self) + 1 :]
        dif = n - len(cells)
        if dif > 0 and cells[-1].connection is not None:
            cells += cells[-1].get_front_cells(dif)
        return cells[:n]
    
class EndpointCell(Cell):
    rate = 0
    connection = None
    
class EndpointEntranceCell(EndpointCell):
    endpoint_rule_class = rules.EntranceRule
    speed = 1
    
class EndpointExitCell(EndpointCell):
    endpoint_rule_class = rules.ExitRule
    
    def get_front_cells(self, n, route=None):
        if self.connection is None:
            return []
        elif isinstance(self.connection, StreetCell):
            return [self.connection] + self.connection.get_front_cells(n - 1)
        elif isinstance(self.connection, IntersectionCell):
            return [self.connection] + self.connection.get_front_cells(n - 1, route)
        else:
            raise NotImplementedError
    
class StreetEntranceCell(EndpointEntranceCell, StreetCell):
    pass
    
class StreetExitCell(EndpointExitCell, StreetCell):
    pass

class IntersectionEntranceCell(EndpointEntranceCell, IntersectionCell):
    pass

class IntersectionExitCell(EndpointExitCell, IntersectionCell):
    pass