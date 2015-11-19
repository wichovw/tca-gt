import cProfile
from pstats import Stats
import io
import csv
from tca_ng import models, example_maps, cars
import random
#
tca = models.Automaton()
topo = example_maps.grid_2lane_map(width=2, height=2)
tca.topology = topo
topo.automaton = tca

for cell in topo.cells:
    if hasattr(cell, 'front_cell') and cell.front_cell is not None:
        cell.front_cell.back_cell = cell
        
topo.foo_cells = []
traces = []
data = {}

for _ in range(2000):
    tca.update()
    for cell in topo.foo_cells:
        data[(cell, tca.generation)] = {
            'count': 0,
            'start': tca.generation,
            'length': 0,
        }
        traces.append({
                'cell': cell,
                'orig': (cell, tca.generation),
                'elim': False,
            })
    topo.foo_cells.clear()
    
    ntraces = []
    for cell in traces:
        data[cell['orig']]['count'] += 1
        if cell['cell'].car is None:
            data[cell['orig']]['length'] += 1
            cell['elim'] = True
            if hasattr(cell['cell'], 'back_cell'):
                ncell = cell['cell'].back_cell
                if ncell is not None:
                    ntraces.append({
                            'cell': ncell,
                            'orig': cell['orig'],
                            'elim': False
                        })
    traces += ntraces
    
    for cell in traces:
        if cell['elim']:
            traces.remove(cell)
    print(_)
    
with open('blocking_cars.csv', 'w', newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['generation', 'count', 'length'])
    for d, c in data.items():
        writer.writerow([c['start'], c['count'], c['length']])
        
#tca.update()
#car = topo.cars[0]
#for _ in range(1000):
#    if car in topo.cars:
#        print(car.cell.id, car.speed)
#    else:
#        break
#    tca.update()



#print(len(tca.topology.cells))

#with open('profiler_results.csv', 'w', newline='\n') as csvfile:
#    writer = csv.writer(csvfile)
#    for _ in range(1000):
#        cProfile.run('tca.update()', filename='tca_profiling')
#        stream = io.StringIO()
#        stats = Stats('tca_profiling', stream=stream)
#        stats.print_stats(0)
#        s = stream.getvalue()
#        secs_pos = s.find('seconds')
#        time = s[secs_pos-6:secs_pos-1]
#    
#        writer.writerow([len(tca.topology.cars), time])
#        print(_, time)
#

#with open('velosity_results.csv', 'w', newline='\n') as csvfile:
#    writer = csv.writer(csvfile)
#    tot_cells = len(tca.topology.cells)
#    for _ in range(2000):
#        tca.update()
#        cars = tca.topology.cars
#        cells_moved = sum(c.speed for c in cars)
#        
#        writer.writerow([len(cars), tot_cells, cells_moved])
#        print(_, cells_moved)

#total_cells = []
#
#size = 100
#steps = 20
#
#for d in range(steps-1):
#    
#    sc = (size//steps) * (d+1)
#    
#    tca = models.Automaton()
#    topo = example_maps.generate_street(size, rate=1)
#    tca.topology = topo
#    topo.automaton = tca
#
#    cells = [{'density': 0, 'flow': 0, 'car': None} for c in sorted(topo.cells, key=lambda x: x.id)]
#
#    topo.cells[0].connection = topo.cells[-1]
#    topo.cells[-1].connection = topo.cells[0]
#    topo.cells[-1].front_cell = topo.cells[0]
#    m_cells = [c for c in topo.cells]
#    
#    for _ in range(sc):
#        cell = random.choice(m_cells)
#        car = cars.Car()
#        car.cell = cell
#        car.speed = 0
#        car.v_max = 1
#        cell.car = car
#        cell.street.car_entry(car)
#        topo.cars.append(car)
#        m_cells.remove(cell)
#
#    for _ in range(1000):
#        tca.update()
#
#        for i, cell in enumerate(sorted(topo.cells, key=lambda x: x.id)):
#            if cell.car is not None:
#                cells[i]['density'] += 1 
#                if cell.car.id != cells[i]['car']:
#                    cells[i]['flow'] += 1 
#                cells[i]['car'] = cell.car.id
#            else:
#                cells[i]['car'] = None
#
#        print(sc, _)
#        
#    total_cells.extend(cells)
#
#with open('velosity_results.csv', 'w', newline='\n') as csvfile:
#    writer = csv.writer(csvfile)
#    tot_cells = len(tca.topology.cells)
#
#    writer.writerow(['density', 'flow'])
#    for cell in total_cells:
#        writer.writerow([cell['density'], cell['flow']])

