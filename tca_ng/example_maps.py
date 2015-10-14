import tca_ng.cells
import tca_ng.models


def generate_street(length, rate=0.8):
    topo = tca_ng.models.Topology()
    
    entrance = tca_ng.cells.StreetEntranceCell()
    topo.cells.append(entrance)
    topo.endpoint_cells.append(entrance)
    for _ in range(length - 2):
        topo.cells.append(tca_ng.cells.StreetCell())
    exit = tca_ng.cells.StreetExitCell()
    topo.cells.append(exit)
    topo.endpoint_cells.append(exit)
    
    street = tca_ng.models.Street()
    street.cells.append([])

    for i, cell in enumerate(topo.cells):
        street.cells[0].append(cell)
        cell.topology = topo
        cell.viewer_address = [i, 0]
        cell.street = street
        cell.lane = 0
        cell.cell = i
        cell.cells_to_end = length - i
        if i + 1 < len(topo.cells):
            tca_ng.cells.front_cell = topo.cells[i + 1]
        if isinstance(cell, tca_ng.cells.EndpointCell):
            cell.rate = rate

    # Eddy
    topo.streets.append(street)
            
    return topo


def simple_intersection(rate=0.8):
    topo = tca_ng.models.Topology()
    """
           v
         
           1
    >   0  4  2
           3
    """
    topo.cells = []
    topo.cells.append(tca_ng.cells.IntersectionEntranceCell())
    topo.cells.append(tca_ng.cells.IntersectionEntranceCell())
    topo.cells.append(tca_ng.cells.IntersectionExitCell())
    topo.cells.append(tca_ng.cells.IntersectionExitCell())
    topo.cells.append(tca_ng.cells.IntersectionCell())
    
    int_ = tca_ng.models.Intersection()
    
    routes = []
    int_.routes = routes
    routes.append(tca_ng.models.Route())
    routes.append(tca_ng.models.Route())
    routes.append(tca_ng.models.Route())
    routes.append(tca_ng.models.Route())
    
    routes[0].cells = [topo.cells[0], topo.cells[4], topo.cells[2]]
    routes[1].cells = [topo.cells[0], topo.cells[4], topo.cells[3]]
    routes[2].cells = [topo.cells[1], topo.cells[4], topo.cells[3]]
    routes[3].cells = [topo.cells[1], topo.cells[4], topo.cells[2]]
    
    topo.cells[0].viewer_address = [0, 1]
    topo.cells[0].topology = topo
    topo.cells[0].intersection = int_
    topo.cells[0].routes = [routes[0], routes[1]]
    topo.cells[0].rate = rate
    
    topo.cells[1].viewer_address = [1, 0]
    topo.cells[1].topology = topo
    topo.cells[1].intersection = int_
    topo.cells[1].routes = [routes[2], routes[3]]
    topo.cells[1].rate = rate
    
    topo.cells[2].viewer_address = [2, 1]
    topo.cells[2].topology = topo
    topo.cells[2].intersection = int_
    topo.cells[2].routes = [routes[0], routes[3]]
    topo.cells[2].rate = rate
    
    topo.cells[3].viewer_address = [1, 2]
    topo.cells[3].topology = topo
    topo.cells[3].intersection = int_
    topo.cells[3].routes = [routes[1], routes[2]]
    topo.cells[3].rate = rate
    
    topo.cells[4].viewer_address = [1, 1]
    topo.cells[4].topology = topo
    topo.cells[4].intersection = int_
    topo.cells[4].routes = [routes[0], routes[1], routes[2], routes[3]]
    
    semaphore = tca_ng.models.Semaphore()
    int_.semaphore = semaphore
    topo.semaphores = [semaphore,]
    lights = []
    semaphore.lights = lights
    topo.lights = lights

    # Eddy
    topo.intersections.append(int_)
    
    lights.append(tca_ng.models.Light())
    lights.append(tca_ng.models.Light())

    lights[0].viewer_address = [0, 2]
    lights[0].routes = [routes[0], routes[1]]
    
    lights[1].viewer_address = [0, 0]
    lights[1].routes = [routes[2], routes[3]]
    
    semaphore.topology = topo
    semaphore.set_schedule({
            0: lights[0],
            20: lights[1],
    })
    
    return topo


def simple_map(size=5):
    topo = tca_ng.models.Topology()
    
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
        
    for cell in int_.cells + int_.lights:
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

    # Eddy
    int_o.in_streets.append(streets[0].cells[0].street)
    int_o.in_streets.append(streets[1].cells[0].street)
    int_o.out_streets.append(streets[2].cells[0].street)
    int_o.out_streets.append(streets[3].cells[0].street)

        
    for street in streets:
        topo.cells += street.cells
    topo.cells += int_.cells
    topo.endpoint_cells = [
        streets[0].cells[0],
        streets[1].cells[0],
        streets[2].cells[-1],
        streets[3].cells[-1],
    ]
        
    topo.lights = int_.lights
    topo.semaphores = int_.semaphores

    for cell in topo.cells:
        cell.topology = topo
    for semaphore in topo.semaphores:
        semaphore.topology = topo
        
    return topo


def totito_map(size=5):
    topo = tca_ng.models.Topology()
    
    crosses = []
    crosses.append(simple_map(size))
    crosses.append(simple_map(size))
    crosses.append(simple_map(size))
    crosses.append(simple_map(size))
    
    side = size * 2 + 2
    for cell in crosses[1].cells + crosses[1].lights:
        y = cell.viewer_address[1]
        cell.viewer_address[1] = side - cell.viewer_address[0]
        cell.viewer_address[0] = y + side + 1
    for cell in crosses[2].cells + crosses[2].lights:
        cell.viewer_address[0] = side * 2 - cell.viewer_address[0] + 1
        cell.viewer_address[1] = side * 2 - cell.viewer_address[1] + 1
    for cell in crosses[3].cells + crosses[3].lights:
        x = cell.viewer_address[0]
        cell.viewer_address[0] = side - cell.viewer_address[1]
        cell.viewer_address[1] = x + side + 1
        
    crosses[0].cells[3 * size - 1].connection = crosses[1].cells[size]
    crosses[2].cells[3 * size - 1].connection = crosses[3].cells[size]
    crosses[0].cells[4 * size - 1].connection = crosses[3].cells[0]
    crosses[2].cells[4 * size - 1].connection = crosses[1].cells[0]
    
    crosses[0].cells[3 * size - 1].front_cell = crosses[1].cells[size]
    crosses[2].cells[3 * size - 1].front_cell = crosses[3].cells[size]
    crosses[0].cells[4 * size - 1].front_cell = crosses[3].cells[0]
    crosses[2].cells[4 * size - 1].front_cell = crosses[1].cells[0]
    
    crosses[1].cells[size].connection = crosses[0].cells[3 * size - 1]
    crosses[3].cells[size].connection = crosses[2].cells[3 * size - 1]
    crosses[3].cells[0].connection = crosses[0].cells[4 * size - 1]
    crosses[1].cells[0].connection = crosses[2].cells[4 * size - 1]
    
    for cross in crosses:
        topo.cells += cross.cells
        topo.lights += cross.lights
        topo.semaphores += cross.semaphores
        
    topo.endpoint_cells = [
        crosses[0].cells[0],
        crosses[0].cells[size],
        crosses[1].cells[3 * size - 1],
        crosses[1].cells[4 * size - 1],
        crosses[2].cells[0],
        crosses[2].cells[size],
        crosses[3].cells[3 * size - 1],
        crosses[3].cells[4 * size - 1],
    ]
    
    for cell in topo.cells:
        cell.topology = topo
    for semaphore in topo.semaphores:
        semaphore.topology = topo
    
    return topo
    
        
def simple_2_streets(size=5):
    topo = tca_ng.models.Topology()
    
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
    
    for cell in topo.cells:
        cell.topology = topo
        
    return topo
