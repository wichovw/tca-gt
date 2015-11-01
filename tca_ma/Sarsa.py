import random
import math

specs = [
  {"negative":False,"start":0,"width":5.0,"size":30,"res": 0.5},
  {"negative":False,"start":0,"width":10.0,"size":30,"res": 1.0},
  {"negative":True,"start":-5,"width":0.5,"size":30,"res": 0.05}
]

class Sarsa(object):
    def __init__(self, actions, epsilon=0.1, alpha=0.2, gamma=0.9):
        self.q = {"change":{},"stay":{}}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions
        

    def getQ(self, state, action,):
        return self.q[action].get(state, 0.0)
        
        

    def learnQ(self, state, action, reward, value):
        oldv = self.q[action].get(state, None)
        if oldv is None:
            self.q[action][state] = reward 
        else:
            self.q[action][state] = oldv + self.alpha * (value - oldv)

    def chooseAction(self, state):
        if random.random() < self.epsilon:
            action = random.choice(self.actions)
        else:
            q = []
            for a in self.actions:
              q.append(self.getQ(state,a))
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)

            action = self.actions[i]
        print ("Action selected: "+action)
        # print (self.q)
        return action

    def learn(self, state1, action1, reward, state2, action2):
        qnext = self.getQ(state2, action2)
        self.learnQ(state1, action1, reward, reward + self.gamma * qnext)

   #Discretize state
    def activeTile(self,state):
      
      tiles = []
      print(state)
      
      coord = []
      dim = 0
      for i in specs:
        length = i["width"]*i["size"]
        cell = (state[dim]-i["start"])/i["width"]

        coord.append(str(math.floor(cell)))
        dim+=1
      # print(coord)
      coord = ",".join(coord)
      
      return coord
    
    #Active tiles for tile coding
    def activeTiles(self,state,tilings=10):
      
      tiles = []
      
      for tiling in range(tilings):
        coord = []
        dim = 0
        for i in specs:
          
          length = i["width"]*i["size"]
          cell = length/state[dim]
          if i["negative"]:
            cell = cell + i["res"]*tiling if tiling<tilings/2 else cell - i["res"]*tiling
          else:
            cell = cell - i["res"]*tiling
          coord.append(math.floor(cell))
          dim+=1
        coord = ",".join(coord)
        tiles.append(coord)
      return tiles
    
    #Tile coding
    def weightSum(self,tiles):
      
      totalWeight = 0
      for key in tiles:
        if self.matrix.has_key(key):
          totalWeight+=self.matrix[key]
        else:
          self.matrix[key]=0
        
      return totalWeight
        