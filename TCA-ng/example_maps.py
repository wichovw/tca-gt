import cells
import models

def generate_street(length, rate=0.8):
    topo = models.Topology()
    
    entrance = cells.StreetEntranceCell()
    topo.cells.append(entrance)
    topo.endpoint_cells.append(entrance)
    for _ in range(length - 2):
        topo.cells.append(cells.StreetCell())
    exit = cells.StreetExitCell()
    topo.cells.append(exit)
    topo.endpoint_cells.append(exit)
    
    street = models.Street()
    street.cells.append([])
        
    for i, cell in enumerate(topo.cells):
        street.cells[0].append(cell)
        cell.viewer_address = [i, 0]
        cell.street = street
        cell.lane = 0
        cell.cell = i
        cell.cells_to_end = length - i
        if i + 1 < len(topo.cells):
            cells.front_cell = topo.cells[i + 1]
        if isinstance(cell, cells.EndpointCell):
            cell.rate = rate
            
    return topo

def simple_intersection(rate=0.8):
    topo = models.Topology()
    """
           v
         
           1
    >   0  4  2
           3
    """
    topo.cells = []
    topo.cells.append(cells.IntersectionEntranceCell())
    topo.cells.append(cells.IntersectionEntranceCell())
    topo.cells.append(cells.IntersectionExitCell())
    topo.cells.append(cells.IntersectionExitCell())
    topo.cells.append(cells.IntersectionCell())
    
    int_ = models.Intersection()
    
    routes = []
    int_.routes = routes
    routes.append(models.Route())
    routes.append(models.Route())
    routes.append(models.Route())
    routes.append(models.Route())
    
    routes[0].cells = [topo.cells[0], topo.cells[4], topo.cells[2]]
    routes[1].cells = [topo.cells[0], topo.cells[4], topo.cells[3]]
    routes[2].cells = [topo.cells[1], topo.cells[4], topo.cells[3]]
    routes[3].cells = [topo.cells[1], topo.cells[4], topo.cells[2]]
    
    topo.cells[0].viewer_address = [0, 1]
    topo.cells[0].intersection = int_
    topo.cells[0].routes = [routes[0], routes[1]]
    topo.cells[0].rate = rate
    
    topo.cells[1].viewer_address = [1, 0]
    topo.cells[1].intersection = int_
    topo.cells[1].routes = [routes[2], routes[3]]
    topo.cells[1].rate = rate
    
    topo.cells[2].viewer_address = [2, 1]
    topo.cells[2].intersection = int_
    topo.cells[2].routes = [routes[0], routes[3]]
    topo.cells[2].rate = rate
    
    topo.cells[3].viewer_address = [1, 2]
    topo.cells[3].intersection = int_
    topo.cells[3].routes = [routes[1], routes[2]]
    topo.cells[3].rate = rate
    
    topo.cells[4].viewer_address = [1, 1]
    topo.cells[4].intersection = int_
    topo.cells[4].routes = [routes[0], routes[1], routes[2], routes[3]]
    
    return topo
        
def simple_map(size=5):
    topo = models.Topology()
    
    streets = []
    streets.append(generate_street(size))
    streets.append(generate_street(size))
    streets.append(generate_street(size))
    streets.append(generate_street(size))
    
    int_ = simple_intersection()
    
    streets[0].cells[0].street.routes = int_.cells[0].routes
    streets[1].cells[0].street.routes = int_.cells[0].routes
    
    for cell in streets[0].cells:
        cell.viewer_address[1] += size + 1
    for cell in streets[2].cells:
        cell.viewer_address[0] += size + 3
        cell.viewer_address[1] += size + 1
        
    for cell in streets[1].cells:
        x = cell.viewer_address[0]
        cell.viewer_address[0] = size + 1
        cell.viewer_address[1] = x
    for cell in streets[3].cells:
        x = cell.viewer_address[0]
        cell.viewer_address[0] = size + 1
        cell.viewer_address[1] = x + size + 3
        
    for cell in int_.cells:
        cell.viewer_address[0] += size
        cell.viewer_address[1] += size
        
    streets[0].cells[-1].connection = int_.cells[0]
    streets[1].cells[-1].connection = int_.cells[1]
    streets[2].cells[0].connection = int_.cells[2]
    streets[3].cells[0].connection = int_.cells[3]
    
    int_.cells[0].connection = streets[0].cells[-1]
    int_.cells[1].connection = streets[1].cells[-1]
    int_.cells[2].connection = streets[2].cells[0]
    int_.cells[3].connection = streets[3].cells[0]
    
    streets[0].cells[-1].front_cell = int_.cells[0]
    streets[1].cells[-1].front_cell = int_.cells[1]
    
    int_o = int_.cells[0].intersection
    streets[0].cells[0].street.exit_routes.extend([int_o.routes[0], int_o.routes[1]])
    streets[1].cells[0].street.exit_routes.extend([int_o.routes[2], int_o.routes[3]])
        
    for street in streets:
        topo.cells += street.cells
    topo.cells += int_.cells
    topo.endpoint_cells = [
        streets[0].cells[0],
        streets[1].cells[0],
        streets[2].cells[-1],
        streets[3].cells[-1],
    ]
        
    return topo
        
def simple_2_streets(size=5):
    topo = models.Topology()
    
    street1 = generate_street(size)
    street2 = generate_street(size)
    
    for cell in street2.cells:
        cell.viewer_address[0] += size
    
    exit = street1.cells[size - 1]
    entrance = street2.cells[0]
    
    exit.connection = entrance
    entrance.connection = exit
    
    exit.front_cell = entrance
    
    topo.cells = street1.cells + street2.cells
    topo.endpoint_cells = [street1.cells[0], street2.cells[size - 1]]
    return topo