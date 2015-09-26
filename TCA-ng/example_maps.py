import cells
import random

class Route:
    cells = []

class Street:
    cells = []
    exit_routes = []
    
    def get_route(self):
        return random.choice(self.exit_routes)
    
class Topology:
    cells = []
    endpoint_cells = []
    
    def text_view(self):
        max_x = 0
        max_y = 0
        for cell in self.cells:
            max_x = max(max_x, cell.viewer_address[0] + 1)
            max_y = max(max_y, cell.viewer_address[1] + 1)

        grid = [[""]*max_x for _ in range(max_y)]

        for cell in self.cells:
            grid[cell.viewer_address[1]][cell.viewer_address[0]] = 0 if not cell.car else 1
#            grid[cell.viewer_address[1]][cell.viewer_address[0]] = cell.id

        string = ""
        for y in grid:
            for x in y:
                string += "%3s" % x
            string += "\n"
            
        return string
    
def simple_street(rate=0.8):
    topo = Topology()
    
    # cells declaration
    topo.cells.append(cells.StreetEntranceCell())
    topo.cells.append(cells.StreetCell())
    topo.cells.append(cells.StreetCell())
    topo.cells.append(cells.StreetExitCell())
    
    topo.endpoint_cells = [topo.cells[0], topo.cells[3]]
    
    street = Street()
    street.cells = [[topo.cells[0], topo.cells[1], topo.cells[2], topo.cells[3]]]
    
    # cells definition
    
    topo.cells[0].viewer_address = (0, 0)
    topo.cells[0].street = street
    topo.cells[0].lane = 0
    topo.cells[0].cell = 0
    topo.cells[0].cells_to_end = 3
    topo.cells[0].front_cell = topo.cells[1]
    
    topo.cells[1].viewer_address = (1, 0)
    topo.cells[1].street = street
    topo.cells[1].lane = 0
    topo.cells[1].cell = 1
    topo.cells[1].cells_to_end = 2
    topo.cells[1].front_cell = topo.cells[2]
    
    topo.cells[2].viewer_address = (2, 0)
    topo.cells[2].street = street
    topo.cells[2].lane = 0
    topo.cells[2].cell = 2
    topo.cells[2].cells_to_end = 1
    topo.cells[2].front_cell = topo.cells[3]
    
    topo.cells[3].viewer_address = (3, 0)
    topo.cells[3].street = street
    topo.cells[3].lane = 0
    topo.cells[3].cell = 3
    topo.cells[3].cells_to_end = 0
    topo.cells[3].front_cell = None
    
    topo.cells[0].rate = rate
    topo.cells[3].rate = rate
    
    return topo