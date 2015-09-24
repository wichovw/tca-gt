class Light:
    """An individual traffic light located at the end of a street. Belongs to
    a semaphore"""
    
    def __init__(self, street, time=50):
        self.color = 0
        self.street = street
        self.time = time
        # TODO Add unique ID
        self.id = None

class Semaphore:
    """a group of syncronized traffic lights that coordinate on the same 
    intersection"""
    
    def __init__(self, intersection, street=None, time=50):
        intersection.semaphore = self
        self.lights = []
        self.green_index = 0
        self.counter = 0
        if street:
            self.add(street, time=time)
            
    def add(self, street, time=50):
        light = Light(street, time=time)
        self.lights.append(light)
        street.light = light
        
    def update(self):
        green = self.lights[self.green_index]
        if self.counter >= green.time:
            green.color = 0
            self.green_index = (self.green_index + 1) % len(self.lights)
            green = self.lights[self.green_index]
            green.color = 1
            self.counter = 0
        self.counter += 1
        
    def start(self):
        for light in self.lights:
            light.color = 0
        self.lights[self.green_index].color = 1