import cherrypy, cherrypy_cors, os
import example_maps

class TCAServer(object):
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def start(self):
        self.automaton = example_maps.Automaton()
        self.automaton.topology = example_maps.simple_street()
        return self.automaton.topology.json_view()
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update(self):
        self.automaton.update()
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