import cells

class Route:
    cells = []

class Topology:
    cells = []
    
def print_topo(topo):
    max_x = 0
    max_y = 0
    for cell in topo.cells:
        max_x = max(max_x, cell.viewer_address[0] + 1)
        max_y = max(max_y, cell.viewer_address[1] + 1)
        
    grid = [[""]*max_x for _ in range(max_y)]
    
    for cell in topo.cells:
        grid[cell.viewer_address[1]][cell.viewer_address[0]] = cell.state - 1
        
    for y in grid:
        for x in y:
            print("%3s" % x, end=' ')
        print()
    
def populate_topo():
    topo = Topology()
    
    # cells declaration
    topo.cells.append(cells.EndpointCell())
    topo.cells.append(cells.EndpointCell())
    topo.cells.append(cells.EndpointCell())
    topo.cells.append(cells.EndpointCell())
    topo.cells.append(cells.IntersectionCell())
    topo.cells.append(cells.IntersectionCell())
    topo.cells.append(cells.IntersectionCell())
    topo.cells.append(cells.IntersectionCell())
    topo.cells.append(cells.IntersectionCell())
    topo.cells.append(cells.StreetCell())
    topo.cells.append(cells.StreetCell())
    topo.cells.append(cells.StreetCell())
    topo.cells.append(cells.StreetCell())
    topo.cells.append(cells.StreetCell())
    topo.cells.append(cells.StreetCell())
    topo.cells.append(cells.StreetCell())
    topo.cells.append(cells.StreetCell())
    
    # routes declaration
    routes = []
    routes.append(Route())
    routes.append(Route())
    routes.append(Route())
    routes.append(Route())
    
    # routes definition
    routes[0].cells = [topo.cells[4], topo.cells[8], topo.cells[6]]
    routes[1].cells = [topo.cells[4], topo.cells[8], topo.cells[5]]
    routes[2].cells = [topo.cells[7], topo.cells[8], topo.cells[5]]
    routes[3].cells = [topo.cells[7], topo.cells[8], topo.cells[6]]
    
    # endpoint cells definition
    
    topo.cells[0].viewer_address = (4, 0)
    topo.cells[0].type_ = cells.MAP_ENTRANCE_CELL
    topo.cells[0].rate = 0.5
    
    topo.cells[1].viewer_address = (8, 4)
    topo.cells[1].type_ = cells.MAP_EXIT_CELL
    topo.cells[1].rate = 0.5
    
    topo.cells[2].viewer_address = (4, 8)
    topo.cells[2].type_ = cells.MAP_EXIT_CELL
    topo.cells[2].rate = 0.5
    
    topo.cells[3].viewer_address = (0, 4)
    topo.cells[3].type_ = cells.MAP_ENTRANCE_CELL
    topo.cells[3].rate = 0.5
    
    # intersection cells definition
    
    topo.cells[4].viewer_address = (4, 3)
    topo.cells[4].type_ = cells.INT_ENTRANCE_CELL
    topo.cells[4].routes = [routes[0], routes[1]]
    topo.cells[4].indexes = [0, 0]
    
    topo.cells[5].viewer_address = (5, 4)
    topo.cells[5].type_ = cells.INT_EXIT_CELL
    topo.cells[5].routes = [routes[1], routes[2]]
    topo.cells[4].indexes = [2, 2]
    
    topo.cells[6].viewer_address = (4, 5)
    topo.cells[6].type_ = cells.INT_EXIT_CELL
    topo.cells[6].routes = [routes[0], routes[3]]
    topo.cells[4].indexes = [2, 2]
    
    topo.cells[7].viewer_address = (3, 4)
    topo.cells[7].type_ = cells.INT_ENTRANCE_CELL
    topo.cells[7].routes = [routes[2], routes[3]]
    topo.cells[4].indexes = [0, 0]
    
    topo.cells[8].viewer_address = (4, 4)
    topo.cells[8].type_ = cells.INT_INNER_CELL
    topo.cells[8].routes = [routes[0], routes[1], routes[2], routes[3]]
    topo.cells[4].indexes = [1, 1, 1, 1]
    
    # street cells definition
    
    topo.cells[9].viewer_address = (4, 1)
    topo.cells[9].lane = 0
    topo.cells[9].cell_from_start = 0
    topo.cells[9].cells_to_end = 1
    topo.cells[9].front_cells = [topo.cells[10], topo.cells[4]]
    topo.cells[9].back_cells = [topo.cells[0]]
    
    topo.cells[10].viewer_address = (4, 2)
    topo.cells[10].lane = 0
    topo.cells[10].cell_from_start = 1
    topo.cells[10].cells_to_end = 0
    topo.cells[10].front_cells = [topo.cells[4]]
    topo.cells[10].back_cells = [topo.cells[9], topo.cells[0]]
    
    topo.cells[11].viewer_address = (7, 4)
    topo.cells[11].lane = 0
    topo.cells[11].cell_from_start = 0
    topo.cells[11].cells_to_end = 1
    topo.cells[11].front_cells = [topo.cells[12], topo.cells[5]]
    topo.cells[11].back_cells = [topo.cells[1]]
    
    topo.cells[12].viewer_address = (6, 4)
    topo.cells[12].lane = 0
    topo.cells[12].cell_from_start = 1
    topo.cells[12].cells_to_end = 0
    topo.cells[12].front_cells = [topo.cells[5]]
    topo.cells[12].back_cells = [topo.cells[11], topo.cells[1]]
    
    topo.cells[13].viewer_address = (4, 7)
    topo.cells[13].lane = 0
    topo.cells[13].cell_from_start = 0
    topo.cells[13].cells_to_end = 1
    topo.cells[13].front_cells = [topo.cells[14], topo.cells[6]]
    topo.cells[13].back_cells = [topo.cells[2]]
    
    topo.cells[14].viewer_address = (4, 6)
    topo.cells[14].lane = 0
    topo.cells[14].cell_from_start = 1
    topo.cells[14].cells_to_end = 0
    topo.cells[14].front_cells = [topo.cells[6]]
    topo.cells[14].back_cells = [topo.cells[13], topo.cells[2]]
    
    topo.cells[15].viewer_address = (1, 4)
    topo.cells[15].lane = 0
    topo.cells[15].cell_from_start = 0
    topo.cells[15].cells_to_end = 1
    topo.cells[15].front_cells = [topo.cells[16], topo.cells[7]]
    topo.cells[15].back_cells = [topo.cells[3]]
    
    topo.cells[16].viewer_address = (2, 4)
    topo.cells[16].lane = 0
    topo.cells[16].cell_from_start = 1
    topo.cells[16].cells_to_end = 0
    topo.cells[16].front_cells = [topo.cells[7]]
    topo.cells[16].back_cells = [topo.cells[15], topo.cells[3]]
    
    return topo

def test():
    topo = populate_topo()
    print_topo(topo)

if __name__ == "__main__":
    test()