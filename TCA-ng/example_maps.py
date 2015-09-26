import cells
import random

class Street:
    cells = []
    
class Topology:
    cells = []
    endpoint_cells = []
    
    def get_view(self):
        max_x = 0
        max_y = 0
        for cell in self.cells:
            max_x = max(max_x, cell.viewer_address[0] + 1)
            max_y = max(max_y, cell.viewer_address[1] + 1)

        grid = [[""]*max_x for _ in range(max_y)]

        for cell in self.cells:
            grid[cell.viewer_address[1]][cell.viewer_address[0]] = '.' if not cell.car else cell.car.speed
        return grid
    
    def text_view(self):
        grid = self.get_view()
        string = '\n'.join(''.join('%3s' % x for x in y) for y in grid)
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