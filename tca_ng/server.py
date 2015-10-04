import cherrypy, cherrypy_cors, os
import tca_ng.example_maps
import tca_ng.models
import random


class TCAServer(object):
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def start(self):
        self.automaton = tca_ng.models.Automaton()
        self.automaton.topology = tca_ng.example_maps.totito_map(10)
        return self.automaton.topology.json_view()
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update(self):
        self.automaton.update()
        
        print()
        print('total cars', len(self.automaton.topology.cars))
        for car in self.automaton.topology.cars:
            if car.id % 10 == 0:
                print('car %3s %8s route: %s' % (
                        car.id,
                        tuple(car.cell.viewer_address),
                        car.route
                ))
        
        # modify a light
        light = random.choice(self.automaton.topology.lights)
        change = random.randint(-2, 2)
        print(light, light.time, change)
        light.time += change
        print()
        
        return self.automaton.topology.json_view()
    
PATH = os.path.abspath(os.path.dirname(__file__))


def serve(ip, port):
    cherrypy_cors.install()
    config = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': PATH,
            'tools.staticdir.index': 'index.html',
            'cors.expose.on': True,
            }
        }
    cherrypy.server.socket_host = ip
    cherrypy.server.socket_port = port
    
    cherrypy.quickstart(TCAServer(), '/', config)
    
if __name__ == '__main__':
    serve('localhost', 5555)

