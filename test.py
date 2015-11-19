from tca import parser, base, viewer
import json

def test(map_name, run_viewer=True):
    data = {}
    with open('tca/maps/%s.json' % map_name) as raw_file:
        data = json.load(raw_file)
    topo = parser.parse(data)
    print('map %s loaded' % data['topology']['name'])
    
    print('cells:', len(data['topology']['cells']))
    print('endpoints:', len(data['topology']['endpoints']))
    print('intersections:', len(data['topology']['intersections']))
    print('lights:', len(data['topology']['lights']))
    print('routes:', len(data['topology']['routes']))
    print('semaphores:', len(data['topology']['semaphores']))
    print('streets:', len(data['topology']['streets']))
    
    tca = base.Automaton(topo)
    viewer.start(tca)
    
if __name__ == '__main__':
    test('grid16')

#    from tca_ng import test
#    test.test()