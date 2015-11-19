from tca_ng import models, cells

def parse(data):
    
    # Assert topology is well formed
        
    topology_ = data['topology']
    topology = models.Topology()
    
    street_objs = {}
    for street_ in topology_['streets']:
        # Assert street is well formed
        street = models.Street()
        street.length = street_['length']
        street.lanes = street_['lanes']
        for lane in range(street.lanes + 1):
            street.cells.append([])
        topology.streets.append(street)
        street_objs[street_['name']] = street
        street.meta = street_
        
    cell_objs = {}
    for cell_ in topology_['cells']:
        # Assert cell is well formed
        cell = getattr(cells, cell_['type'])()
        cell.viewer_address = cell_['viewer_address']
        if 'street' in cell_:
            # Assert street data is well formed
            street = street_objs[cell_['street']]
            cell.street = street
            cell.lane = cell_['lane']
            cell.cell = cell_['cell']
            cell.cells_to_end = street.length - cell.cell
            street.cells[cell.lane].append(cell)
        topology.cells.append(cell)
        cell.topology = topology
        cell_objs[cell_['name']] = cell
        cell.meta = cell_
        
    int_objs = {}
    for int_ in topology_['intersections']:
        # Assert intersection is well formed
        intr = models.Intersection()
        topology.intersections.append(intr)
        int_objs[int_['name']] = intr
        intr.meta = int_
    
    route_objs = {}
    for route_ in topology_['routes']:
        # Assert route is well formed
        route = models.Route()
        int_objs[route_['intersection']].routes.append(route)
        route.entrance_lane = route_['entrance_lane']
        for cell_name in route_['cells']:
            route.cells.append(cell_objs[cell_name])
            cell_objs[cell_name].routes.append(route)
            cell_objs[cell_name].intersection = int_objs[route_['intersection']]
        route_objs[route_['name']] = route
        route.meta = route_
        
    sem_objs = {}
    for sem_ in topology_['semaphores']:
        # Assert semaphore is well formed
        sem = models.Semaphore()
        sem.topology = topology
        int_objs[sem_['intersection']].semaphore = sem
        topology.semaphores.append(sem)
        sem_objs[sem_['name']] = sem
        sem.meta = sem_
    
    light_objs = {}
    for light_ in topology_['lights']:
        # Assert light is well formed
        light = models.Light()
        light.viewer_address = light_['viewer_address']
        for route_name in light_['routes']:
            light.routes.append(route_objs[route_name])
        sem_objs[light_['semaphore']].lights.append(light)
        topology.lights.append(light)
        light_objs[light_['name']] = light
        light.meta = light_
        
    for sem in sem_objs.values():
        sch = {}
        for time, light_name in sem.meta['schedule'].items():
            # Assert times
            sch[int(time)] = light_objs[light_name]
        sem.set_schedule(sch)
        
    for cell_ in topology_['endpoints']:
        cell = cell_objs[cell_['cell']]
        cell.rate = cell_['rate']
        topology.endpoint_cells.append(cell)
        
    for cell in cell_objs.values():
        for conn, cell_name in cell.meta['neighbours'].items():
            setattr(cell, conn, cell_objs[cell_name])
            
    for street in street_objs.values():
        for route_name in street.meta['exit_routes']:
            street.exit_routes.append(route_objs[route_name])
    
    return topology

def render(topology, name='map'):
    
    data = {}
    data['name'] = name
        
    data['cells'] = []
    for cell in topology.cells:
        cell_ = {
            'name': cell.id,
            'type': str(cell.__class__).split('.')[-1][:-2],
            'viewer_address': cell.viewer_address,
            'neighbours': {}
        }
        if hasattr(cell, 'street'):
            cell_['street'] = cell.street.id
            cell_['lane'] = cell.lane
            cell_['cell'] = cell.cell
        front_cell = getattr(cell, 'front_cell', None)
        right_cell = getattr(cell, 'right_cell', None)
        left_cell = getattr(cell, 'left_cell', None)
        connection = getattr(cell, 'connection', None)
        if front_cell is not None:
            cell_['neighbours']['front_cell'] = front_cell.id
        if right_cell is not None:
            cell_['neighbours']['right_cell'] = right_cell.id
        if left_cell is not None:
            cell_['neighbours']['left_cell'] = left_cell.id
        if connection is not None:
            cell_['neighbours']['connection'] = connection.id
        data['cells'].append(cell_)
    
    data['streets'] = []
    for street in topology.streets:
        data['streets'].append({
                'name': street.id,
                'length': street.length,
                'lanes': street.lanes,
                'exit_routes': [r.id for r in street.exit_routes]
            })
        
    print(len(data['streets']))
        
    data['intersections'] = []
    data['routes'] = []
    data['semaphores'] = []
    data['lights'] = []
    for intr in topology.intersections:
        for route in intr.routes:
            data['routes'].append({
                    'name': route.id,
                    'intersection': intr.id,
                    'cells': [c.id for c in route.cells],
                    'entrance_lane': route.entrance_lane
                })
        data['intersections'].append({
                'name': intr.id,
            })
        sem_ = {
            'name': intr.semaphore.id,
            'intersection': intr.id,
            'schedule': {}
        }
        for k, light in intr.semaphore.get_schedule().items():
            sem_['schedule'][k] = light.id
        data['semaphores'].append(sem_)
        for light in intr.semaphore.lights:
            data['lights'].append({
                    'name': light.id,
                    'semaphore': intr.semaphore.id,
                    'viewer_address': light.viewer_address,
                    'routes': [r.id for r in light.routes],
                })
            
    data['endpoints'] = []
    for cell in topology.endpoint_cells:
        data['endpoints'].append({
                'cell': cell.id,
                'rate': cell.rate
            })
        
    return {'topology': data}