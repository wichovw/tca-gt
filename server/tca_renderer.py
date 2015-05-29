
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
    