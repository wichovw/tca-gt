
def renderStreet(map, street_id=0):
    graph = []
    street = map.streets[street_id]
    
#    graph.append([-2 for _ in range(street.height)])
    for lane in range(street.width):
        row = []
        for cell in range(street.height):
            val = street.get((lane, cell))
            row.append(-1 if val == 0 else val.speed)
        graph.append(row)
#    graph.append([-2 for _ in range(street.height)])
    
    return graph
    
    
def renderIntersection(map, hstreet_id=0, vstreet_id=1):
    graph = []
    horizontal = map.streets[hstreet_id]
    vertical = map.streets[vstreet_id]
    hfront = map.streets[horizontal.front_id]
    vfront = map.streets[vertical.front_id]
    
    width = horizontal.height + horizontal.front_offset + hfront.height
    height = vertical.height + vertical.front_offset + vfront.height
    
    graph = [[-2] * width for _ in range(height)]
    
    for lane in range(horizontal.width):
        for cell in range(horizontal.height + horizontal.front_offset):
            val = horizontal.get((lane, cell))
            y = lane + vertical.height
            x = cell
            graph[x][y] = -1 if val == 0 else val.speed
            
    for lane in range(hfront.width):
        for cell in range(hfront.height):
            val = hfront.get((lane, cell))
            y = lane + vertical.height
            x = cell + horizontal.height + horizontal.front_offset
            graph[x][y] = -1 if val == 0 else val.speed
            
    for lane in range(vertical.width):
        for cell in range(vertical.height):
            val = vertical.get((lane, cell))
            x = lane + horizontal.height
            y = cell
            if vertical.orientation == 3:
                x = width - x - 1
            if vertical.orientation == 1:
                y = height - y - 1
            graph[x][y] = -1 if val == 0 else val.speed
            
    for lane in range(vertical.width):
        for cell in range(vfront.height):
            val = vfront.get((lane, cell))
            x = lane + horizontal.height
            y = cell + vertical.height + vertical.front_offset
            if vertical.orientation == 3:
                x = width - x - 1
            if vertical.orientation == 1:
                y = height - y - 1
            graph[x][y] = -1 if val == 0 else val.speed
    
    return graph