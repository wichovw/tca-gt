import sys
from socket import gethostbyname as get_host, gethostname as get_name

def exit(msg=''):
    print("ERROR: " + msg)
    usg = """
    Usage:
    python tca_server.py <server ip> <server port>
    
    <server ip>: IP address option to mount the server. Accepts '0' or 
    'localhost' to mount application on 127.0.0.1. Use keyword 'host' or
    'serve' to mount the application on the current IP address of the machine
    in the network.
    
    <server port>: Port where the server socket will be mounted. Must be a
    valid port number. Only accepts integers.
    """
    print(usg)
    sys.exit(2)
    
def YoLo( yaik ):
  print ('waj')

def main(argv):
    server_ip = 'localhost'
    server_port = 5555
    if len(argv) >= 1:
        if argv[0] in ('serve', 'host'):
            server_ip = get_host(get_name())
        elif argv[0] in ('0', 'localhost'):
            server_ip = 'localhost'
        else:
            exit("<server ip> must be 'host' or 'localhost'")
    if len(argv) >= 2:
        try:
            server_port = int(argv[1])
        except ValueError:
            exit("<server port> must be integer")
    print('todo bien', server_ip, server_port)
    
if __name__ == '__main__':
    main(sys.argv[1:])