import tca_ng.rules


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
    topology = None
    
    def __init__(self):
        self.id = Cell.id
        Cell.id += 1
    
    def __repr__(self):
        return "<Cell: %s (%s)>" % (self.id, '.' if self.car is None else self.car.speed)
    
    def apply_rules(self):
        self.car = self.p.car


class StreetCell(Cell):
    rule_class = tca_ng.rules.StreetRule
    street = None
    lane = None
    cell = None
    cells_to_end = None
    front_cell = None
    right_cell = None
    left_cell = None
    
    def get_front_cells(self, n, route=None):
        cells = self.street.cells[self.lane][self.cell + 1 :]
        dif = n - len(cells)
        if dif > 0 and cells[-1].connection is not None:
            cells += cells[-1].get_front_cells(dif, route)
        return cells[:n]


class IntersectionCell(Cell):
    rule_class = tca_ng.rules.IntersectionRule
    routes = None
    intersection = None
    
    def __init__(self):
        super().__init__()
        self.routes = []
    
    def get_front_cells(self, n, route=None):
        if route is None:
            return []
#            route = self.intersection.get_valid_route(self)
        cells = route.cells[route.cells.index(self) + 1 :]
        dif = n - len(cells)
        if dif > 0 and cells[-1].connection is not None:
            cells += cells[-1].get_front_cells(dif, route)
        return cells[:n]


class EndpointCell(Cell):
    rate = 0
    connection = None


class EndpointEntranceCell(EndpointCell):
    endpoint_rule_class = tca_ng.rules.EntranceRule
    speed = 1


class EndpointExitCell(EndpointCell):
    endpoint_rule_class = tca_ng.rules.ExitRule
    
    def get_front_cells(self, n, route=None):
        if self.connection is None:
            return []
        elif isinstance(self.connection, StreetCell):
            return [self.connection] + self.connection.get_front_cells(n - 1, route)
        elif isinstance(self.connection, IntersectionCell):
            if (route in self.connection.intersection.semaphore.get_active_light().routes
                and route in self.connection.routes):
                return [self.connection] + self.connection.get_front_cells(n - 1, route)
            else:
                return []
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