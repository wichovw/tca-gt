from tca_ma.ITA import ITA
from tca_ma.CTA import CTA
from tca_ma.LTA import LTA
from service.tca_service import TCAService


def main():
  service = TCAService()
  infoAgent = ITA(service)
  coordAgent = CTA(infoAgent)
  localAgents = []
  for i in service.get_intersections():
    localAgents.append(LTA(i['id'],infoAgent,coordAgent))
    
  service.set_cycle_size(5)
  
  while service.get_actual_iteration() < 1000:
    infoAgent.updateSchedule()
    infoAgent.update()
    input("Good luck:"+str(service.get_actual_iteration()))
    for agent in localAgents:
      print("\n\nEnter Agent "+str(agent.id)+"\n\n")
      agent.update()
    
    avg_speed = 0.0
    for key, value in infoAgent.dynamic.items():
      avg_speed+=value['avg_speed']
    
    print("TOTAL: "+ str(avg_speed/len(localAgents)))
    

  
    

  
  
    
if __name__ == '__main__':
    main()