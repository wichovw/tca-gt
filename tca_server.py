import sys
sys.path.append('server')
from server.main import main

def serve(argv):
    main(argv)

if __name__ == '__main__':
    serve(sys.argv[1:])