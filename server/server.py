import os
import cherrypy, cherrypy_cors
from server.tca_parser import create_map, parse
from server.tca_renderer import GridMapRenderer
from server.tca.map import TCAMap
from server.tca.automaton import TCAAutomaton

class TCAServer(object):
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def start(self, size=2):
#        matrix = create_map(rows, cols)
        matrix = parse('totito')
        map = TCAMap(matrix)
        self.automaton = TCAAutomaton(map)
        self.render = GridMapRenderer(map)
        return self.render.get_matrix()
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update(self):
        self.automaton.update()
        return self.render.get_matrix()

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