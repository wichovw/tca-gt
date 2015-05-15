import tca.cellaut as ca

ca.GridTopology.background = 0
ca.GridTopology.border = None

class StreetTopology(ca.GridTopology):
    
    def __init__(self, id, lanes, length, front):
        self.id = id
        self.front_id = front[0]
        super().__init__((lanes, length))
        
class TCATopology(ca.Topology):
    
    border = None
    
    def __init__(self, map):
        self.description = map
        self.streets = {}
        for street in map['streets']:
            if street['id'] not in self.streets:
                top = StreetTopology(street['id'], street['lanes'], street['length'], street['front'])
                self.streets[street['id']] = top
            else:
                raise ValueError("Duplicated street id: %s" % self.id)
        # look for streets on the back
        for street_id, street in self.streets.items():
            back_street = None
            for sid, strt in self.streets.items():
                if strt.front_id == street_id:
                    street.back_id = sid
                    break
            
        for car in map['cars']:
            address = (car['streetId'], car['lane'], car['cell'])
            state = (car['speed'], 0, 0)
            self.set(address, state)
    
    def normalize(self, address):
        street, lane, cell = address
        if type(street) != StreetTopology:
            street = self.streets.get(street, None)
        if not street:
            raise IndexError
        addr = street.normalize((lane, cell))
        if not addr:
            if lane < 0 or lane >= street.width:
                return None
            elif cell < 0:
                back = self.streets.get(street.back_id, None)
                if not back:
                    return None
                return self.normalize((street.back_id, lane, cell + back.height))
            else:
                return self.normalize((street.front_id, lane, cell - street.height))
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