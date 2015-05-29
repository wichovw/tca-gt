import os
import cherrypy, cherrypy_cors
from tca_parser import parse
from tca_renderer import renderStreet, renderIntersection
from tca.map import TCAMap
from tca.automaton import TCAAutomaton

class TCAServer(object):
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def start(self, map='intersection'):
        matrix = parse(map)
        map = TCAMap(matrix)
        self.automaton = TCAAutomaton(map)
#        return renderStreet(self.automaton.map, street_id=0)
        return renderIntersection(self.automaton.map, hstreet_id=0, vstreet_id=1)
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update(self):
        self.automaton.update()
#        return renderStreet(self.automaton.map, street_id=0)
        return renderIntersection(self.automaton.map, hstreet_id=0, vstreet_id=1)

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