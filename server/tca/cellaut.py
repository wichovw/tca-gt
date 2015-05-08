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