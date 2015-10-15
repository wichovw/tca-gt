# TCA.gt
Traffic Cellular Automata for Guatemala City

## New Generation
1. Crear ng\_env haciendo virtualenv con requirements\_ng.txt
	1. Puede que no funcione instalar pygame, (a mi no me funcionó sólo con pip install) hacer referencia a [esta respuesta de Stack Overflow](http://stackoverflow.com/a/28127864).
2. Activar ng\_env.
2. Correr tca\_server.py que se encuentra en el folder root para correr el simulador.

## Install and use
1. Create a virtual environment and activate it. [More info here](http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/).

   ```shell
   # windows users:
   >> pip install virtualenv
   >> cd code\myproject
   >> virtualenv env
   >> env\Scripts\activate
   
   # unix users:
   $ sudo pip install virtualenv
   $ cd code/myproject/
   $ virtualenv env
   $ source env/bin/activate
   ```
   
1. Make sure all the project dependencies are met. (Mac users, note that you don't need to `sudo` any more).

   ```shell
   $ pip install -r requirements.txt
   ```
   
1. Put the backend server to run.

   ```shell
   # serve on localhost:5555 (default)
   $ python tca_server.py
   
   # serve on localhost:1234
   $ python tca_server.py 0 1234
   
   # serve on the network, with host ip and port 1234
   $ python tca_server.py host 1234
   ```
   
1. Get the frontend server working. Be aware to set the actual back-server ip and port. Defaults are `localhost:5555`.

   ```shell
   # serve on localhost:4200 (default)
   $ python front_server.py
   
   # serve on localhost:1234 and configure backend to 192.168.1.2:9999
   $ python front_server.py 0 1234 192.168.1.2 9999
   ```
