import json

def parse(map):
    with open('server/maps/%s.json' % map) as data_file:    
        data = json.load(data_file)
    return data

def create_map(size, lanes=2, length=20):
    total_streets = (size + 1) * size * 2
    street_to_east = 0
    street_to_west = int(total_streets / 4)
    street_to_south = int(total_streets / 2)
    street_to_north = int(total_streets / 4 * 3)
    turn_dir = 0
    for i in range(total_streets):
        if i % (size + 1) == 0:
            generator = True
            
        
#    south_id = rows * (cols + 1)
#    north_id = south_id + (rows * 2)
#    turn_id = [south_id, north_id]
#    dir_ = 0        #east
#    turn_dir = 0    #south
#    turn_name = ['right', 'left']
#    for row in range(rows):
#        street_base_id = row * (cols + 1)
#        turn_id = [t + 1 for t in turn_id]
#        row_turn_id = turn_id
#        for i in range(cols):
#            street_id = street_base_id + i
#            turn = turn_name[(dir_ + turn_dir) % 2]
#            street = {
#                "id": street_id,
#                "lanes": lanes,
#                "length": length,
#                "generate": False,
#                "front": {
#                    "straight": street_id + 1,
#                    turn: row_turn_id[turn_dir],
#                    "offset": lanes
#                }
#            }
#            if i == 0:
#                street["generate"] = True
#            
#            row_turn_id[turn_dir] += (cols + 1) * 2 * (-1 if turn_dir == 1 else 1)
#            turn_dir = (turn_dir + 1) % 2
#            print(street)
            
#create_map(4)