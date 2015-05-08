import os
import cherrypy
import cherrypy_cors
from map_parser import parse
from tca.automatons import TCAAutomaton

class TCAServer(object):
    exposed = True
    
    def start(self, map='basic'):
        matrix = parse(map)
        self.automaton = TCAAutomaton(matrix)
        

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