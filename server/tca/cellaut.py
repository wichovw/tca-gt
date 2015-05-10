# Based on cage v1.1.4
# http://www.alcyone.com/software/cage/
# Copyright (C) 2002-2006 Erik Max Francis <max@alcyone.com>
# GPL License

class Topology:
    """Encaptulation of the shape and dimentionality of a cellular automata"""
    
    def get(self, address):
        raise NotImplementedError
        
    def set(self, address, state):
        raise NotImplementedError
        
    def normalize(self, address):
        raise NotImplementedError
            
class Neighborhood:
    """Abstraction of the set of cells adjacent to any given cell"""
    
    def neighbors(self, address):
        """Returns a list of addresses which are neighbors."""
        raise NotImplementedError
        
    def states(self, address):
        """Returns the list of cell values for all neighbors"""
        return [self.get(x) for x in self.neighbors(address)]
                  
class GridTopology(Topology):
    """A two dimentional, bounded topology consisting of a rectangular grid
    of cells"""
    
    background = 0
    border = 0
    
    def __init__(self, size):
        self.width, self.height = size
        self.buffer = []
        for _ in range(self.width):
            self.buffer.append([self.background] * self.height)
            
    def normalize(self, address):
        x, y = address
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return address
    
    def get(self, address):
        addr = self.normalize(address)
        if addr:
            x, y = addr
            return self.buffer[x][y]
        else:
            return self.border
        
    def set(self, address, state):
        addr = self.normalize(address)
        if addr:
            x, y = addr
            self.buffer[x][y] = state
        else:
            raise IndexError

class ExtendedNeighborhood(Neighborhood):
    """A neighborhood that retrieves a list of states on each direction"""
    
    def states(self, address, max=1):
        return [[self.get(i) for i in j] for j in self.neighbors(address, max)]
    
class Automaton:
    """Abstraction for the actions that can be made over the different cells
    and states of a specified map"""
    
    def __init__(self, map):
        self.map = map
        self.generation = 0
        
    def update(self):
        self.generation += 1
        
class Rule:
    """Definition of rules to follow to change a cell value in an automaton"""
    
    def __init__(self, map, address):
        self.populate(map, address)
        
    def populate(self, map, address):
        raise NotImplementedError
        
    def apply(self):
        raise NotImplementedError