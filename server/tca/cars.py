import uuid

class Car:
    speed = 0
    change_lane_intention = 0
    street = None
    
    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            self.id = str(uuid.uuid4())
        if 'speed' in kwargs:
            self.speed = kwargs['speed']
        if 'change_lane_intention' in kwargs:
            self.change_lane_intention = kwargs['change_lane_intention']
        if 'street' in kwargs:
            street = kwargs['street']
            
    def clone(self):
        return Car(id=self.id,
                   speed=self.speed,
                   change_lane_intention=self.change_lane_intention,
                   street=self.street
                  )
    
    def __repr__(self):
        return "<Car [%s] s:%d>" % (self.id[:4], self.speed)