import random
import math
from service.tca_service import TCAService


class ITA(object):
  def __init__(self,service):
    self.service = service
    self.dynamic = None
    self.newSchedule = None
    self.timeInterval = 5
    self.intersections = {}
    for i in self.service.get_intersections():
      self.intersections[i['id']] = i
    traffic_lights = self.service.get_traffic_lights()
    for key, value in self.intersections.items():
      for j in traffic_lights:
        if key==j['id']:
          self.intersections[key]['schedule'] = j['schedule']
          
          self.intersections[key]['green_light_id'] = j['schedule'][0]
          
          self.intersections[key]['lights'] = j['lights']
        
    

  def update(self):
    self.dynamic = {}
    self.newSchedule = []

    for avg in self.service.dynamic_time_update():
      street = {}
      street['avg_speed'] = avg['average_speed']
      street['cars_number'] = avg['cars_number']
      street['green_light'] = avg['green_light']
      
   
      
      self.dynamic[avg['id']] = street

   # print(self.dynamic)
    
    
  def updateSchedule(self):
    print(self.newSchedule)
    self.service.set_traffic_lights(self.newSchedule)


  def getSpeed(self,agentID):
    intersection = self.intersections[agentID]
    speed = {}
    for i in intersection['in_streets']:
      speed[i] = self.dynamic[i]

    return speed
    
    
  def schedule(self,agentID):
    intersection = self.intersections[agentID]
    schedule = {}
    for i in intersection['lights']:
      if(i != intersection['green_light_id']):
        self.intersections[agentID]['green_light_id'] = i
        
        
        schedule[0] = self.intersections[agentID]['green_light_id']
        

        
    
    self.newSchedule.append({'id':agentID,'schedule':schedule})
    return 1

  def neighbours(self,intersection):
    return self.intersections[intersection]['out_streets']

    
    
  def getTimeInterval(self):
    return self.timeInterval
    
    
  def getLightStreet(self,agentID):
    # return self.intersections[agentID][light]
    intersection = self.intersections[agentID]
 
    lights = {}
    for i in intersection['in_streets']:
      
      if self.dynamic[i]['green_light'] == 0:
        lights['red'] = i
      else:
        lights['green'] = i

    return lights
    
      