import random
import math
from service.tca_service import TCAService


class CTA(object):
  def __init__(self,ITA):
    self.ITA = ITA
    
  #Comapare with neighbours if there is a congestion to stop vehicles from keep going
  def validate(self,agentID):
    neighbours = self.ITA.neighbours(agentID)
    density = []
    for i in neighbours:
     
      density.append(self.ITA.dynamic[i]['cars_number']/(self.ITA.dynamic[i]['avg_speed']+0.1))
    
    #The value of 100 is arbitrary. Can be changed find better results
    if max(density)<100:
      return 1
    else:
      return 0
    # return self.ITA.schedule(agentID)
    