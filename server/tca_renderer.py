
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
            graph[x][y] = -1 if val == 0 else val.id[:6]
            
    for lane in range(hfront.width):
        for cell in range(hfront.height):
            val = hfront.get((lane, cell))
            y = lane + vertical.height
            x = cell + horizontal.height + horizontal.front_offset
            graph[x][y] = -1 if val == 0 else val.id[:6]
            
    for lane in range(vertical.width):
        for cell in range(vertical.height):
            val = vertical.get((lane, cell))
            x = lane + horizontal.height
            y = cell
            if vertical.orientation == 3:
                x = width - x - 1
            if vertical.orientation == 1:
                y = height - y - 1
            graph[x][y] = -1 if val == 0 else val.id[:6]
            
    for lane in range(vertical.width):
        for cell in range(vfront.height):
            val = vfront.get((lane, cell))
            x = lane + horizontal.height
            y = cell + vertical.height + vertical.front_offset
            if vertical.orientation == 3:
                x = width - x - 1
            if vertical.orientation == 1:
                y = height - y - 1
            graph[x][y] = -1 if val == 0 else val.id[:6]
            
    # traffic lights
    
    graph[horizontal.height - 4][vertical.height - 2] = '00ff00' if horizontal.light.color > 0 else 'ff0000'
    graph[horizontal.height - 4][vertical.height + horizontal.width + 1] = '00ff00' if horizontal.light.color > 0 else 'ff0000'
    graph[horizontal.height - 4][vertical.height - 1] = '00ff00' if horizontal.light.color > 0 else 'ff0000'
    graph[horizontal.height - 4][vertical.height + horizontal.width] = '00ff00' if horizontal.light.color > 0 else 'ff0000'
    vlight = vertical.height - 4 if vertical.orientation == 3 else vfront.height + horizontal.width + 4
    graph[horizontal.height - 2][vlight] = '00ff00' if vertical.light.color > 0 else 'ff0000'
    graph[horizontal.height + vertical.width + 1][vlight] = '00ff00' if vertical.light.color > 0 else 'ff0000'
    graph[horizontal.height - 1][vlight] = '00ff00' if vertical.light.color > 0 else 'ff0000'
    graph[horizontal.height + vertical.width][vlight] = '00ff00' if vertical.light.color > 0 else 'ff0000'
    
    return graph

class GridMapRenderer:
    
    def __init__(self, map):
        self.streets = map.clone().streets
        self.map = map
        init_street = self.streets.pop(0, None)
        self.min_x, self.min_y = 0, 0
        self.max_x, self.max_y = 0, 0
        map_ = self.create_map(init_street)
        self.map_ = self.normalize(map_)
        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y
        
#        for s in map_:
#            print(
#                s['street'].id,
#                s['initial'],
#                s['orientation']
#            )
#            
#        print((self.min_x, self.min_y), (self.max_x, self.max_y))
        
    def create_map(self, street, initial=(0, 0), orientation=0):
        streets_desc = []
        streets_desc.append({
            'street': self.map.streets[street.id],
            'initial': initial,
            'orientation': orientation,
        })
        streets_out = [
            (street.front_id, 0),
            (street.front['right'], 1),
            (street.front['left'], 3),
            (street.back_id, 4)
        ]
        axe, sign, ox, oy = 0, 1, 0, 0
        i_width, i_height = street.front_offset, street.width
        if orientation in [1, 3]:
            axe = 1
            i_width, i_height = i_height, i_width
        if orientation in [1, 2]:
            ox = -i_width + 1
        if orientation in [2, 3]:
            sign = -1
            oy = -i_height + 1
        intersection_address = list(initial)
        intersection_address[axe] += sign * street.height
        intersection_address[0] += ox
        intersection_address[1] += oy
        for street_out in streets_out:
            new_street = self.streets.pop(street_out[0], None)
            if new_street:
                new_orientation = (orientation + street_out[1]) % 4
                min_x, min_y = 0, 0
                max_x, max_y = 0, 0
                if new_orientation == 0:
                    new_initial = [i_width, 0]
                    max_x = new_street.height + new_street.front_offset
                elif new_orientation == 1:
                    new_initial = [i_width - 1, i_height]
                    max_y = new_street.height + new_street.front_offset
                elif new_orientation == 2:
                    new_initial = [-1, i_height - 1]
                    min_x = -(new_street.height + new_street.front_offset)
                elif new_orientation == 3:
                    new_initial = [0, -1]
                    min_y = -(new_street.height + new_street.front_offset)
                if street_out[1] == 4:
                    val = street.height + new_street.height + new_street.front_offset
                    if new_orientation in [0, 1]:
                        val *= -1
                    new_initial[new_orientation % 2] += val
                addr = (
                    intersection_address[0]+new_initial[0],
                    intersection_address[1]+new_initial[1]
                )
                self.min_x = min(self.min_x, addr[0] + min_x)
                self.min_y = min(self.min_y, addr[1] + min_y)
                self.max_x = max(self.max_x, addr[0] + max_x)
                self.max_y = max(self.max_y, addr[1] + max_y)
                streets_desc.extend(self.create_map(
                        new_street,
                        initial=addr,
                        orientation=new_orientation
                ))
        return streets_desc
    
    def normalize(self, map_):
        offset_x = -self.min_x
        offset_y = -self.min_y
        for s in map_:
            initial = list(s['initial'])
            initial[0] += offset_x
            initial[1] += offset_y
            s['initial'] = tuple(initial)
        return map_
    
    def get_matrix(self):
        matrix = [[-2] * self.height for _ in range(self.width)]
        for street_ in self.map_:
            street = street_['street']
            axe = 0 if street_['orientation'] in [0, 2] else 1
            sign = 1 if street_['orientation'] in [0, 1] else -1
            initial = street_['initial']
            for lane in range(street.width):
                for cell in range(street.height + street.front_offset):
                    val = street.get((lane, cell))
                    addr = list(initial)
                    addr[axe] += cell * sign
                    addr[(axe + 1) % 2] += lane * sign * (1 if axe == 0 else -1)
                    matrix[addr[0]][addr[1]] = -1 if val == 0 else val.id[:6]
            # traffic light
            addr = list(initial)
            addr[axe] += (street.height - 2) * sign
            addr[(axe + 1) % 2] += street.width * sign * (1 if axe == 0 else -1)
            matrix[addr[0]][addr[1]] = '00ff00' if street.light.color > 0 else 'ff0000'
            addr[(axe + 1) % 2] += sign * (1 if axe == 0 else -1)
            matrix[addr[0]][addr[1]] = '00ff00' if street.light.color > 0 else 'ff0000'
            addr[axe] -= sign
            matrix[addr[0]][addr[1]] = '00ff00' if street.light.color > 0 else 'ff0000'
            addr[(axe + 1) % 2] -= sign * (1 if axe == 0 else -1)
            matrix[addr[0]][addr[1]] = '00ff00' if street.light.color > 0 else 'ff0000'
        return matrix