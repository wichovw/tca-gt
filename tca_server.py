#import sys
#sys.path.append('server')
#from server.main import main
#
#def serve(argv):
#    main(argv)
#
#if __name__ == '__main__':
#    serve(sys.argv[1:])

#from tca_ng import server
#    
#if __name__ == '__main__':
#    server.serve('localhost', 5555)

from viewer_ng import test

if __name__ == '__main__':
    test.test()