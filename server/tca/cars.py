import uuid
import random

class Car:
    speed = 0
    change_lane_intention = 0
    street = None
    probability = {}
    
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
            self.street = kwargs['street']

        # probability
        self.probability['random_slow_p'] = random.random()
        self.probability['change_lane_p'] = random.random()
        self.probability['turn_street_p'] = random.random()


    def clone(self):
        return Car(id=self.id,
                   speed=self.speed,
                   change_lane_intention=self.change_lane_intention,
                   street=self.street
                  )

    def get_personality_color(self):
        """
        Return a representative color based on personality
        :return: hex color
        """
        r = lambda: random.randint(0, 255)
        return '#%02X%02X%02X' % (r(), r(), r())
    
    def __repr__(self):
        return "<Car [%s] s:%d>" % (self.id[:4], self.speed)