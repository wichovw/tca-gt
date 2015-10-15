import os
import cherrypy

PATH = os.path.abspath(os.path.dirname(__file__))


class Root(object): pass
		


config={
	'/': {
					'tools.staticdir.on': True,
					'tools.staticdir.dir': PATH,
					'tools.staticdir.index': 'index.html',
			},
  
}

#cherrypy.server.socket_host = '172.20.11.29'
cherrypy.config.update({'server.socket_host': 'localhost',
                        'server.socket_port': 7891,
                       })
cherrypy.quickstart(Root(),'/',config)
