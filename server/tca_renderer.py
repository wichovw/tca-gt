
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
    
    width = horizontal.height + horizontal.front_offset
    height = vertical.height + vertical.front_offset
    
    fill = (int((width - vertical.width) / 2),
            int((height - horizontal.width) / 2))
    
    graph = [[-2] * width for _ in range(height)]
    
    for lane in range(horizontal.width):
        for cell in range(width):
            val = horizontal.get((lane, cell))
            y = lane + fill[1]
            x = (cell + fill[0] + vertical.width) % height
            graph[x][y] = -1 if val == 0 else val.speed
            
    for lane in range(vertical.width):
        for cell in range(height):
            val = vertical.get((lane, cell))
            x = lane + fill[0]
            y = (cell + fill[1] + horizontal.width) % width
            if vertical.orientation == 3:
                x = width - x - 1
            graph[x][y] = -1 if val == 0 else val.speed
            
#    graph2 = []
#    for y in range(len(graph[0])):
#        r = []
#        for x in range(len(graph)):
#            r.append(graph[x][y])
#        graph2.append(r)
    
    return graph