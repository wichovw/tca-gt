import cellaut as ca

class StreetTopology(ca.GridTopology):
    objects = {}
    
    def __init__(self, **kwargs):
        self.id = kwargs[id]
        if StreetTopology.objects.get(self.id, None):
            raise ValueError("Duplicated street id: %s" % self.id)
            
        super().__init__(kwargs[lanes], kwargs[length])
        StreetTopology.objects[self.id] = self
        
class TCATopology(ca.Topology):
    
    def __init__(self, map):
        pass

class TCAAutomaton:
    pass