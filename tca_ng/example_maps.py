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
    
    street.length = length
    street.lanes = 1
        
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

def generate_wide_street(length, lanes, rate=0.8):
    topo = tca_ng.models.Topology()
    
    for _ in range(lanes):
        entrance = tca_ng.cells.StreetEntranceCell()
        topo.cells.append(entrance)
        topo.endpoint_cells.append(entrance)
    for _ in range(length - 2):
        for __ in range(lanes):
            topo.cells.append(tca_ng.cells.StreetCell())
    for _ in range(lanes):
        exit = tca_ng.cells.StreetExitCell()
        topo.cells.append(exit)
        topo.endpoint_cells.append(exit)
    
    street = tca_ng.models.Street()
    for _ in range(lanes):
        street.cells.append([])
        
    street.length = length
    street.lanes = lanes
        
    lane = 0
    for i, cell in enumerate(topo.cells):
        street.cells[lane].append(cell)
        cell.topology = topo
        cell.viewer_address = [i//lanes, lane]
        cell.street = street
        cell.lane = lane
        cell.cell = i // lanes
        cell.cells_to_end = length - cell.cell
        if i + 1 < len(topo.cells) - lanes:
            cell.front_cell = topo.cells[i + lanes]
        if lane + 1 < lanes:
            cell.right_cell = topo.cells[i + 1]
        if lane > 0:
            cell.left_cell = topo.cells[i - 1]
        if isinstance(cell, tca_ng.cells.EndpointCell):
            cell.rate = rate
        lane = (lane + 1) % lanes

    # Eddy
    topo.streets.append(street)

    return topo

def simple_intersection(rate=0.8):
    topo = tca_ng.models.Topology()
    """
           v
         
           1
    >   0  4  2   >
           3
           
           v
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
    
    routes[0].entrance_lane = 0
    routes[1].entrance_lane = 0
    routes[2].entrance_lane = 0
    routes[3].entrance_lane = 0
    
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

def simple_2lane_intersection(rate=0.8):
    topo = tca_ng.models.Topology()
    """
           v  v
         
           3  2
    >   0  8 10  4   >
    >   1  9 11  5   >
           7  6
           
           v  v
    """
    topo.cells = []
    for _ in range(4):
        topo.cells.append(tca_ng.cells.IntersectionEntranceCell())
    for _ in range(4):
        topo.cells.append(tca_ng.cells.IntersectionExitCell())
    for _ in range(4):
        topo.cells.append(tca_ng.cells.IntersectionCell())
        
    int_ = tca_ng.models.Intersection()
    
    routes = []
    int_.routes = routes
    for _ in range(6):
        routes.append(tca_ng.models.Route())
    
    routes[0].cells = [topo.cells[0], topo.cells[8], topo.cells[10], topo.cells[4]]
    routes[1].cells = [topo.cells[1], topo.cells[9], topo.cells[11], topo.cells[5]]
    routes[2].cells = [topo.cells[1], topo.cells[9], topo.cells[7]]
    routes[3].cells = [topo.cells[3], topo.cells[8], topo.cells[9], topo.cells[7]]
    routes[4].cells = [topo.cells[2], topo.cells[10], topo.cells[11], topo.cells[6]]
    routes[5].cells = [topo.cells[2], topo.cells[10], topo.cells[4]]
    
    routes[0].entrance_lane = 0
    routes[1].entrance_lane = 1
    routes[2].entrance_lane = 1
    routes[3].entrance_lane = 1
    routes[4].entrance_lane = 0
    routes[5].entrance_lane = 0
    
    for cell in topo.cells:
        cell.topology = topo
        cell.intersection = int_
        cell.rate = rate
        cell.routes = []
        
    for route in routes:
        for cell in route.cells:
            cell.routes.append(route)
    
    topo.cells[0].viewer_address = [0, 1]
    topo.cells[1].viewer_address = [0, 2]
    topo.cells[2].viewer_address = [2, 0]
    topo.cells[3].viewer_address = [1, 0]
    topo.cells[4].viewer_address = [3, 1]
    topo.cells[5].viewer_address = [3, 2]
    topo.cells[6].viewer_address = [2, 3]
    topo.cells[7].viewer_address = [1, 3]
    topo.cells[8].viewer_address = [1, 1]
    topo.cells[9].viewer_address = [1, 2]
    topo.cells[10].viewer_address = [2, 1]
    topo.cells[11].viewer_address = [2, 2]
    
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

    lights[0].viewer_address = [0, 3]
    lights[0].routes = [routes[0], routes[1], routes[2]]
    
    lights[1].viewer_address = [0, 0]
    lights[1].routes = [routes[3], routes[4], routes[5]]
    
    semaphore.topology = topo
    semaphore.set_schedule({
            0: lights[0],
            20: lights[1],
    })
    
    return topo

def simple_2lane_map(size=5):
    topo = tca_ng.models.Topology()
    
    streets = []
    streets.append(generate_wide_street(size, 2))
    streets.append(generate_wide_street(size, 2))
    streets.append(generate_wide_street(size, 2))
    streets.append(generate_wide_street(size, 2))
    
    int_ = simple_2lane_intersection()
    
#    streets[0].cells[0].street.routes = int_.cells[0].routes + int_.cells[1].routes
#    streets[0].cells[0].street.routes = int_.cells[2].routes + int_.cells[3].routes

    for cell in streets[0].cells:
        cell.viewer_address[1] += size + 1
    for cell in streets[2].cells:
        cell.viewer_address[0] += size + 4
        cell.viewer_address[1] += size + 1
        
    for cell in streets[1].cells:
        x = cell.viewer_address[0]
        cell.viewer_address[0] = size - cell.lane + 2
        cell.viewer_address[1] = x
    for cell in streets[3].cells:
        x = cell.viewer_address[0]
        cell.viewer_address[0] = size - cell.lane + 2
        cell.viewer_address[1] = x + size + 4
        
    for cell in int_.cells + int_.lights:
        cell.viewer_address[0] += size
        cell.viewer_address[1] += size
        
    streets[0].cells[-2].connection = int_.cells[0]
    streets[0].cells[-1].connection = int_.cells[1]
    streets[1].cells[-2].connection = int_.cells[2]
    streets[1].cells[-1].connection = int_.cells[3]
    streets[2].cells[0].connection = int_.cells[4]
    streets[2].cells[1].connection = int_.cells[5]
    streets[3].cells[0].connection = int_.cells[6]
    streets[3].cells[1].connection = int_.cells[7]
    
    int_.cells[0].connection = streets[0].cells[-2]
    int_.cells[1].connection = streets[0].cells[-1]
    int_.cells[2].connection = streets[1].cells[-2]
    int_.cells[3].connection = streets[1].cells[-1]
    int_.cells[4].connection = streets[2].cells[0]
    int_.cells[5].connection = streets[2].cells[1]
    int_.cells[6].connection = streets[3].cells[0]
    int_.cells[7].connection = streets[3].cells[1]
    
    streets[0].cells[-2].front_cell = int_.cells[0]
    streets[0].cells[-1].front_cell = int_.cells[1]
    streets[1].cells[-2].front_cell = int_.cells[2]
    streets[1].cells[-1].front_cell = int_.cells[3]
    
    int_o = int_.cells[0].intersection
    streets[0].cells[0].street.exit_routes.extend([int_o.routes[0], int_o.routes[1], int_o.routes[2]])
    streets[1].cells[0].street.exit_routes.extend([int_o.routes[3], int_o.routes[4], int_o.routes[5]])

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
        streets[0].cells[1],
        streets[1].cells[0],
        streets[1].cells[1],
        streets[2].cells[-2],
        streets[2].cells[-1],
        streets[3].cells[-2],
        streets[3].cells[-1],
    ]
        
    topo.lights = int_.lights
    topo.semaphores = int_.semaphores

    for cell in topo.cells:
        cell.topology = topo
    for semaphore in topo.semaphores:
        semaphore.topology = topo
        
    return topo

def simple_map(size=5):
    topo = tca_ng.models.Topology()
    
    streets = []
    streets.append(generate_street(size))
    streets.append(generate_street(size))
    streets.append(generate_street(size))
    streets.append(generate_street(size))
    
    int_ = simple_intersection()
    
#    streets[0].cells[0].street.routes = int_.cells[0].routes
#    streets[1].cells[0].street.routes = int_.cells[0].routes
    
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


def totito_2lane_map(size=5):
    topo = tca_ng.models.Topology()
    
    crosses = []
    crosses.append(simple_2lane_map(size))
    crosses.append(simple_2lane_map(size))
    crosses.append(simple_2lane_map(size))
    crosses.append(simple_2lane_map(size))
    
    side = size * 2 + 3
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
        
    crosses[0].cells[3 * size * 2 - 2].connection = crosses[1].cells[size * 2]
    crosses[0].cells[3 * size * 2 - 1].connection = crosses[1].cells[size * 2 + 1]
    crosses[2].cells[3 * size * 2 - 2].connection = crosses[3].cells[size * 2]
    crosses[2].cells[3 * size * 2 - 1].connection = crosses[3].cells[size * 2 + 1]
    
    crosses[0].cells[4 * size * 2 - 2].connection = crosses[3].cells[0]
    crosses[0].cells[4 * size * 2 - 1].connection = crosses[3].cells[1]
    crosses[2].cells[4 * size * 2 - 2].connection = crosses[1].cells[0]
    crosses[2].cells[4 * size * 2 - 1].connection = crosses[1].cells[1]
    
    crosses[1].cells[size * 2].connection = crosses[0].cells[3 * size * 2 - 2]
    crosses[1].cells[size * 2 + 1].connection = crosses[0].cells[3 * size * 2 - 1]
    crosses[3].cells[size * 2].connection = crosses[2].cells[3 * size * 2 - 2]
    crosses[3].cells[size * 2 + 1].connection = crosses[2].cells[3 * size * 2 - 1]
    
    crosses[1].cells[0].connection = crosses[2].cells[4 * size * 2 - 2]
    crosses[1].cells[1].connection = crosses[2].cells[4 * size * 2 - 1]
    crosses[3].cells[0].connection = crosses[0].cells[4 * size * 2 - 2]
    crosses[3].cells[1].connection = crosses[0].cells[4 * size * 2 - 1]
    
    
    crosses[0].cells[3 * size * 2 - 2].front_cell = crosses[1].cells[size * 2]
    crosses[0].cells[3 * size * 2 - 1].front_cell = crosses[1].cells[size * 2 + 1]
    crosses[2].cells[3 * size * 2 - 2].front_cell = crosses[3].cells[size * 2]
    crosses[2].cells[3 * size * 2 - 1].front_cell = crosses[3].cells[size * 2 + 1]
    
    crosses[0].cells[4 * size * 2 - 2].front_cell = crosses[3].cells[0]
    crosses[0].cells[4 * size * 2 - 1].front_cell = crosses[3].cells[1]
    crosses[2].cells[4 * size * 2 - 2].front_cell = crosses[1].cells[0]
    crosses[2].cells[4 * size * 2 - 1].front_cell = crosses[1].cells[1]
    
    # Eddy
    crosses[0].cells[40].intersection.neighbors.append(crosses[1].cells[40].intersection)
    crosses[2].cells[40].intersection.neighbors.append(crosses[3].cells[40].intersection)
    crosses[0].cells[40].intersection.neighbors.append(crosses[3].cells[40].intersection)
    crosses[2].cells[40].intersection.neighbors.append(crosses[1].cells[40].intersection)
    crosses[1].cells[40].intersection.neighbors.append(crosses[0].cells[40].intersection)
    crosses[3].cells[40].intersection.neighbors.append(crosses[2].cells[40].intersection)
    crosses[3].cells[40].intersection.neighbors.append(crosses[0].cells[40].intersection)
    crosses[1].cells[40].intersection.neighbors.append(crosses[2].cells[40].intersection)
        
    for cross in crosses:
        for cell in cross.endpoint_cells:
            if cell.connection is None:
                topo.endpoint_cells.append(cell)
        topo.cells += cross.cells
        topo.lights += cross.lights
        topo.semaphores += cross.semaphores
        
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

    # Eddy
    crosses[0].cells[40].intersection.neighbors.append(crosses[1].cells[40].intersection)
    crosses[2].cells[40].intersection.neighbors.append(crosses[3].cells[40].intersection)
    crosses[0].cells[40].intersection.neighbors.append(crosses[3].cells[40].intersection)
    crosses[2].cells[40].intersection.neighbors.append(crosses[1].cells[40].intersection)
    crosses[1].cells[40].intersection.neighbors.append(crosses[0].cells[40].intersection)
    crosses[3].cells[40].intersection.neighbors.append(crosses[2].cells[40].intersection)
    crosses[3].cells[40].intersection.neighbors.append(crosses[0].cells[40].intersection)
    crosses[1].cells[40].intersection.neighbors.append(crosses[2].cells[40].intersection)
    
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

def grid_2lane_map(size=5, width=2, height=2):
    topo = tca_ng.models.Topology()
    
    totitos = []
    matrix = []
    for _ in range(height):
        row = []
        matrix.append(row)
        for __ in range(width):
            totito = totito_2lane_map(size)
            row.append(totito)
            totitos.append(totito)
    
    totito_size = size * 4 + 8
    for i in range(height):
        for j in range(width):
            totito = matrix[i][j]
            
            for cell in totito.cells + totito.lights:
                cell.viewer_address[0] += totito_size * j
                cell.viewer_address[1] += totito_size * i
                
            if i > 0:
                totito.cells[10].connection = matrix[i - 1][j].cells[184]
                totito.cells[11].connection = matrix[i - 1][j].cells[185]
                totito.cells[80].connection = matrix[i - 1][j].cells[114]
                totito.cells[81].connection = matrix[i - 1][j].cells[115]
                totito.cells[80].front_cell = matrix[i - 1][j].cells[114]
                totito.cells[81].front_cell = matrix[i - 1][j].cells[115]
            if i < height - 1:
                totito.cells[114].connection = matrix[i + 1][j].cells[80]
                totito.cells[115].connection = matrix[i + 1][j].cells[81]
                totito.cells[184].connection = matrix[i + 1][j].cells[10]
                totito.cells[185].connection = matrix[i + 1][j].cells[11]
                totito.cells[184].front_cell = matrix[i + 1][j].cells[10]
                totito.cells[185].front_cell = matrix[i + 1][j].cells[11]
            if j > 0:
                totito.cells[0].connection = matrix[i][j - 1].cells[90]
                totito.cells[1].connection = matrix[i][j - 1].cells[91]
                totito.cells[194].connection = matrix[i][j - 1].cells[104]
                totito.cells[195].connection = matrix[i][j - 1].cells[105]
                totito.cells[194].front_cell = matrix[i][j - 1].cells[104]
                totito.cells[195].front_cell = matrix[i][j - 1].cells[105]
            if j < width - 1:
                totito.cells[90].connection = matrix[i][j + 1].cells[0]
                totito.cells[91].connection = matrix[i][j + 1].cells[1]
                totito.cells[104].connection = matrix[i][j + 1].cells[194]
                totito.cells[105].connection = matrix[i][j + 1].cells[195]
                totito.cells[90].front_cell = matrix[i][j + 1].cells[0]
                totito.cells[91].front_cell = matrix[i][j + 1].cells[1]
            
            topo.cells += totito.cells
            topo.lights += totito.lights
            topo.semaphores += totito.semaphores
    
    for totito in totitos:
        for cell in totito.endpoint_cells:
            if cell.connection is None:
                topo.endpoint_cells.append(cell)
    
    for cell in topo.cells:
        cell.topology = topo
    for semaphore in topo.semaphores:
        semaphore.topology = topo
        
    return topo