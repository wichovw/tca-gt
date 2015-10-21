import random
import math
from service.tca_service import TCAService
from tca_ma.Sarsa import Sarsa


class LTA(object):
  def __init__(self,id,ITA,CTA):
      self.id = id
      self.actions=["change","stay"]
      self.algorithm = Sarsa(self.actions,0.1, 0.1,0.9)
      self.lastAction = None
      self.score = 0
      
      self.ITA = ITA
      self.CTA = CTA
      
      self.streetLights = None
      
      
      self.greenSpeed = 0.0
      self.redSpeed = 0.0
      self.ratio = 1.0
      
      self.lastChange = 0
      self.secondLast = 0
      


  def update(self):
      
 
      
      self.lastChange+= self.ITA.getTimeInterval()
      self.secondLast+= self.ITA.getTimeInterval()
      
      
      speed = self.ITA.getSpeed(self.id)
      
      self.streetLights = self.ITA.getLightStreet(self.id)
      
      print(self.streetLights)
      
      
      self.greenSpeed = speed[self.streetLights['green']]['avg_speed'] #green
      self.redSpeed = speed[self.streetLights['red']]['avg_speed'] #red
      
      #Reward = negative of the sum of time since last two changes and the number of vehicles
      reward = -(speed[self.streetLights['red']]['cars_number'] + self.lastChange)
      
      
      if self.greenSpeed> self.redSpeed:
        if(self.redSpeed == 0):
          self.ratio  = 5
        else:
          self.ratio = math.log(self.greenSpeed/self.redSpeed)
      else:
        if(self.greenSpeed == 0):
          self.ratio  = -5
        else:
          self.ratio = -math.log(self.redSpeed/self.greenSpeed)
        
      
      
      state = self.algorithm.activeTile([self.lastChange,self.secondLast,self.ratio])
      
      action = self.algorithm.chooseAction(state)
      
      
      
      
      if action=="change":
        #CTA will decide if it's better not changing the lights
        if self.CTA.validate(self.id) == 1:
          self.secondLast = self.lastChange
          self.lastChange = 0
          
          temp = self.streetLights['green']
          self.streetLights['green'] = self.streetLights['red']
          self.streetLights['red'] = temp
          
          self.ITA.schedule(self.id)
          
      if self.lastAction is not None:
          self.algorithm.learn(
              self.lastState, self.lastAction, reward, state, action)
      self.lastState = state
      self.lastAction = action
      