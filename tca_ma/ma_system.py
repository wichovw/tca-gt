import random
import math

matrix ={}
def activeTiles(state,specs,tilings=10):
  
  tiles = []
  
  for tiling in tilings:
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
      
def weightSum(tiles):
  
  totalWeight = 0
  for key in tiles:
    if matrix.has_key(key):
      totalWeight+=matrix[key]
    else:
      matrix[key]=0
    
  return totalWeight
  

specs = [
  {"negative":False,"start":0,"width":5.0,"size":30,"res": 0.5},
  {"negative":False,"start":0,"width":10.0,"size":30,"res": 1.0},
  {"negative":True,"start":0,"width":0.5,"size":30,"res": 0.05}
]
tileCoding(specs,10)
exit()

class Sarsa:
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
        return action

    def learn(self, state1, action1, reward, state2, action2):
        qnext = self.getQ(state2, action2)
        self.learnQ(state1, action1, reward, reward + self.gamma * qnext)

        
        
class Agent:
    def __init__(self):
        self.actions=["change","stay"]
        self.learning = sarsa.Sarsa(
            actions=self.actions, epsilon=0.1, alpha=0.1, gamma=0.9)
        self.lastAction = None
        self.score = 0
        
        self.greenSpeed = 0.0
        self.redSpeed = 0.0
        self.ratio = 1.0

    def colour(self):
        return 'blue'

    def update(self):
        reward = self.calcReward()
        
        # state = self.calcState()
        state = self.activeTiles()
        
        """
          getSpeed<-
          self.greenSpeed = getSpeed
          self.redSpeed = getSpeed
          if self.greenSpeed> self.redSpeed:
            self.ratio = Math.log(self.greenSpeed/self.redSpeed)
          else:
            self.ratio = -Math.log(self.redSpeed/self.greenSpeed)
        """
        
        action = self.learning.chooseAction(state)
        
        
        
        
        
        if self.lastAction is not None:
            self.learning.learn(
                self.lastState, self.lastAction, reward, state, action)
        self.lastState = state
        self.lastAction = action

        here = self.cell
        if here.goal or here.cliff:
            self.cell = startCell
            self.lastAction = None
        else:
            self.goInDirection(action)

    def calcState(self):
        return self.cell.x, self.cell.y

    def calcReward(self):
        self.ratio
        if here.cliff:
            return cliffReward
        elif here.goal:
            self.score += 1
            return goalReward
        else:
            return normalReward

if __name__ == '__main__':
  begin()