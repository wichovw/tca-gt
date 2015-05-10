import cellaut as ca

ca.GridTopology.background = 0
ca.GridTopology.border = None

class StreetTopology(ca.GridTopology):
    
    def __init__(self, id, lanes, length, front):
        self.id = id
        self.front_id = front[0]
        super().__init__(lanes, length)
        
class TCATopology(ca.Topology):
    
    border = None
    
    def __init__(self, map):
        self.description = map
        self.streets = {}
        for street in map.streets:
            if street.id not in self.streets:
                top = StreetTopology(street.id, street.lanes, street.length, street.front)
                self.streets[self.id] = top
            else:
                raise ValueError("Duplicated street id: %s" % self.id)
    
    def normalize(self, address):
        street, lane, cell = address
        if type(street) != StreetTopology:
            street = self.streets.get(street, None)
        if not street:
            raise IndexError
        addr = street.normalize((lane, cell))
        if not addr:
            if lane < 0 or lane >= street.width or cell < 0:
                return None
            else:
                return self.normalize((street.front_id, lane, cell - street.length))
        return (street, addr[0], addr[1])
    
    def get(self, address):
        addr = self.normalize(address)
        if addr:
            street, lane, cell = addr
            return street.get((lane, cell))
        else:
            return border
        
    def set(self, address, state):
        addr = self.normalize(address)
        if addr:
            street, lane, cell = addr
            street.set((lane, cell))
        else:
            raise IndexError
            
class TCANeighborhood(ca.ExtendedNeighborhood):
    """The matrix of neighbors has the following distribution for max=3:
    
    (4, 2) (4, 1) (4, 0) (5, 0) (5, 1) (5, 2)           left lane
    (3, 2) (3, 1) (3, 0)  CELL  (0, 0) (0, 1) (0, 2)    front
    (2, 2) (2, 1) (2, 0) (1, 0) (1, 1) (1, 2)           right lane
    """
    
    def neighbors(self, address, max=1):
        x, y = address
        return [[(x, y + i + 1) for i in range(max)],
                [(x + 1, y + i) for i in range(max)],
                [(x + 1, y - i - 1) for i in range(max)],
                [(x, y - i - 1) for i in range(max)],
                [(x + 1, y - i - 1) for i in range(max)],
                [(x + 1, y + i) for i in range(max)]]
                
class TCAMap(TCATopology, TCANeighborhood):
    
    def __init__(self, map):
        TCATopology.__init__(self, map)
        TCANeighborhood.__init__(self)
        
    def clone(self):
        return TCAMap(self.description)