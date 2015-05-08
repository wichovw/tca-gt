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
        self.streets = {}
        for street in map.streets:
            if street.id not in self.streets:
                top = StreetTopology(street.id, street.lanes, street.length, street.front)
                self.streets[self.id] = top
            else:
                raise ValueError("Duplicated street id: %s" % self.id)
    
    def normalize(self, address):
        street_id, lane, cell = address
        street = self.streets.get(street_id, None)
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