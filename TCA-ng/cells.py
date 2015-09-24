

INT_ENTRANCE_CELL = 1
INT_EXIT_CELL = 2
INT_INNER_CELL = 3

MAP_ENTRANCE_CELL = 4
MAP_EXIT_CELL = 5

class Cell:
    car = None
    viewer_address = None
    generation_rate = 0
    consumption_rate = 0
    
class StreetCell(Cell):
    street = None
    lane = None
    cell_from_start = None
    cells_to_end = None
    front_cells = None
    back_cells = None
    right_cell = None
    left_cell = None
    
class IntersectionCell(Cell):
    type_ = None
    routes = None
    indexes = None
    
    def front_cells(self, route):
        index = self.indexes[routes.index(route)]
        return route.cells[index:]
    
class EndpointCell(Cell):
    type_ = None
    rate = 0
    connection = None