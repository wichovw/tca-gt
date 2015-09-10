import server.tca.cellaut as ca
from server.tca.cars import Car
from server.tca.semaphores import Semaphore, Light
from random import randint

ca.GridTopology.background = 0
ca.GridTopology.border = None

class StreetTopology(ca.GridTopology):
    intersection = None
    orientation = 0
    consumer = False
    generator = False
    
    def __init__(self, id, lanes, length, front, generator=False):
        self.front = {}
        self.back = {'left': None, 'right': None}
        self.id = id
        if front.get('consumer', False):
            self.consumer = True
        if generator:
            self.generator = True
        self.front_id = front.get('straight', None)
        self.front_offset = front.get('offset', 0)
        self.front['right'] = front.get('right', None)
        self.front['left'] = front.get('left', None)
        self.back_id = None
        super().__init__((lanes, length))
        
    def normalize(self, address):
        addr = super().normalize(address)
        if not addr:
            lane, cell = address
            if lane in range(self.width) and cell - self.height in range(self.front_offset):
                return address
        return addr
    
    def normalize_intersection(self, address):
        x, y = address
        y -= self.height
        if x in range(self.width) and y in range(self.front_offset):
            if self.orientation == 0:
                return (x, y)
            elif self.orientation == 1:
                return (self.width - y - 1, x)
            elif self.orientation == 3:
                return (y, self.front_offset - x - 1)
    
    def get(self, address):
        addr = self.normalize(address)
        if addr:
            x, y = addr
            if y < self.height:
                return self.buffer[x][y]
            else:
                return self.intersection.get(self.normalize_intersection(addr))
        else:
            return self.border
        
    def set(self, address, value):
        addr = self.normalize(address)
        if addr:
            x, y = addr
            if y < self.height:
                self.buffer[x][y] = value
            else:
                self.intersection.set(self.normalize_intersection(addr), value)
        else:
            raise IndexError
        
        
class TCATopology(ca.Topology):
    
    border = None
    
    def __init__(self, map):
        self.description = map
        self.streets = {}
        self.semaphores = []
        for street in map['streets']:
            if street['id'] not in self.streets:
                top = StreetTopology(street['id'], street['lanes'], street['length'], street['front'], street['generator'])
                self.streets[street['id']] = top
            else:
                raise ValueError("Duplicated street id: %s" % self.id)
                
        self.zero = (tuple(self.streets.keys())[0], 0, 0)
        
        # look for streets on the back
        for street_id, street in self.streets.items():
            front = self.streets.get(street.front_id, None)
            if front:
                front.back_id = street_id
                
        # create intersections
        for street_id, street in self.streets.items():
            for direction in ['right', 'left']:
                turn = self.streets.get(street.front[direction], None)
                if turn:
                    back = self.streets.get(turn.back_id, None)
                    if back and back.intersection:
                        street.intersection = back.intersection
                        street.orientation = 3 if direction == 'left' else 1
                        street.front_offset = back.width
                        street.intersection.semaphore.add(street)
                        break
            if not street.intersection:
                street.intersection = ca.GridTopology((street.width, street.front_offset))
                semaphore = Semaphore(street.intersection, street)
                self.semaphores.append(semaphore)
            
        # populate cars
        for car in range(map['cars']):
            street_id = randint(0, len(self.streets) - 1)
            street = self.streets[street_id]
            lane = randint(0, street.width - 1)
            cell = randint(0, street.height - 1)
            address = (street_id, lane, cell)
            state = Car(street=street_id)
            state.next_street = street.front_id
            self.set(address, state)
    
    def normalize(self, address):
        street, lane, cell = address
        if type(street) != StreetTopology:
            street = self.streets.get(street, None)
        if not street:
            return None
        addr = street.normalize((lane, cell))
        if not addr:
            if lane < 0 or lane >= street.width:
                return None
            elif cell < 0:
                back = self.streets.get(street.back_id, None)
                if not back:
                    return None
                return self.normalize((street.back_id, lane, cell + back.height + back.front_offset))
            else:
                return self.normalize((street.front_id, lane, cell - street.height - street.front_offset))
        return (street, addr[0], addr[1])
    
    def get(self, address):
        addr = self.normalize(address)
        if addr:
            street, lane, cell = addr
            return street.get((lane, cell))
        else:
            return self.border
        
    def set(self, address, state):
        addr = self.normalize(address)
        if addr:
            street, lane, cell = addr
            street.set((lane, cell), state)
        else:
            raise IndexError
            
    def __str__(self, cars_only=False):
        val = ""
        cars = []
        for street_id, street in self.streets.items():
            color = 'green' if street.light.color > 0 else 'red'
            val += '\nStreet %s: %s' % (street_id, color)
            for lane in range(street.width):
                val += '\n'
                for cell in range(street.height + street.front_offset):
                    state = self.get((street_id, lane, cell))
                    if state:
                        val += state.id[0]
                        cars.append(((street_id, lane, cell), state))
                    else:
                        val += '_'
        if cars_only:
            val = ""
        for address, car in cars:
            val += "\n%10s, [%s] speed:%s, cli:%s, strt:%s" % (address,
                                                             car.id[0],
                                                             car.speed,
                                                             car.change_lane_intention,
                                                             car.street
                                                            )
        val += "\nTotal cars: %s" % len(cars)
        
        return val
            
class TCANeighborhood(ca.ExtendedNeighborhood):
    """The matrix of neighbors has the following distribution for max=3:
    
    (4, 2) (4, 1) (4, 0) (5, 0) (5, 1) (5, 2)           left lane
    (3, 2) (3, 1) (3, 0)  CELL  (0, 0) (0, 1) (0, 2)    front
    (2, 2) (2, 1) (2, 0) (1, 0) (1, 1) (1, 2)           right lane
    """
    
    def neighbors(self, address, max=1):
        s, x, y = address
        return [[(s, x, y + i + 1) for i in range(max)],
                [(s, x + 1, y + i) for i in range(max)],
                [(s, x + 1, y - i - 1) for i in range(max)],
                [(s, x, y - i - 1) for i in range(max)],
                [(s, x - 1, y - i - 1) for i in range(max)],
                [(s, x - 1, y + i) for i in range(max)]]
                
class TCAMap(TCATopology, TCANeighborhood):
    
    def __init__(self, map):
        TCATopology.__init__(self, map)
        TCANeighborhood.__init__(self)
        
    def clone(self):
        return TCAMap(self.description)