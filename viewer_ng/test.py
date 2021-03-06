import pygame
import random
from viewer_ng.image_creator import create_tiles
from tca_ng import cells, models, example_maps, cars
from pygame import locals

#tca = models.Automaton()
#topo = example_maps.grid_2lane_map(width=2, height=2)
#tca.topology = topo
#topo.automaton = tca

#tca.update()
#car = topo.cars[0]
#lista = [0]
#speeds = [0]
#for _ in range(1000):
#    if car in topo.cars:
#        lista.append(car.cell.id)
#        speeds.append(car.speed)
#    else:
#        break
#    tca.update()
#    print(_)
#cells.Cell.id = 0
#
#for s in speeds:
#    print(s)
#    
#print (len(speeds))

def get_color(cell):
    if isinstance(cell, cells.StreetCell):
        color = 'street'
    elif isinstance(cell, cells.IntersectionCell):
        color = 'intersection'
    elif isinstance(cell, cells.EndpointEntranceCell):
        color = 'entrance'
    elif isinstance(cell, cells.EndpointExitCell):
        color = 'exit'
    elif isinstance(cell, models.Light):
        color = 'green' if cell.free else 'red'
#        color = 'oob'
    else:
        color = 'oob'
        
    if isinstance(cell, cells.Cell):
        if cell.car is not None:
            color = 'special_car' if cell.car.id % 10 == 0 else 'car'
#            color = 'car'
#            
#    if isinstance(cell, cells.Cell) and cell.id in lista:
#        color = 'exit'
            
    return color

class Cell:
    location = None
    aut_cell = None
    color = 'oob'
    
    def absolute_location(self, square_size):
        x = self.location[0] * square_size
        y = self.location[1] * square_size
        return (x, y)

class Board:
    automaton = None
    cells = []
    size = None
    
    def __init__(self, automaton):
        self.automaton = automaton
        self.cells = []
        self.map_cells()
        
    def map_cells(self):
        max_x = 0
        max_y = 0
        
        def map_(aut_cell, max_x, max_y):
            max_x = max(max_x, aut_cell.viewer_address[0] + 1)
            max_y = max(max_y, aut_cell.viewer_address[1] + 1)
            cell = Cell()
            cell.aut_cell = aut_cell
            cell.location = aut_cell.viewer_address
            cell.color = get_color(aut_cell)
            self.cells.append(cell)
            return max_x, max_y
            
        for aut_cell in self.automaton.topology.cells:
            max_x, max_y = map_(aut_cell, max_x, max_y)
        for light in self.automaton.topology.lights:
            max_x, max_y = map_(light, max_x, max_y)
        self.size = (max_x, max_y)
        
    def update(self):
        for cell in self.cells:
            cell.color = get_color(cell.aut_cell)
            
    def draw(self, screen, tiles):
        for cell in self.cells:
            screen.blit(
                tiles[cell.color],
                cell.absolute_location(self.square_size)
            )
            
def test():
    create_tiles(square_size)
    pygame.init()
    
    tca = models.Automaton()
#    topo = example_maps.generate_wide_street(60, 4)
#    topo = example_maps.grid_2lane_map()
    topo = example_maps.totito_map(10)
#    topo = example_maps.generate_street(25)
    tca.topology = topo
    topo.automaton = tca
    board = Board(tca)
    
#    topo.cells[0].connection = topo.cells[-1]
#    topo.cells[-1].connection = topo.cells[0]
#    topo.cells[-1].front_cell = topo.cells[0]
#    m_cells = [c for c in topo.cells]
#    for _ in range(5):
#        cell = random.choice(m_cells)
#        car = cars.Car()
#        car.cell = cell
#        car.speed = 0
#        car.v_max = 1
#        cell.car = car
#        cell.street.car_entry(car)
#        topo.cars.append(car)
#        m_cells.remove(cell)
    
    width = board.size[0] * square_size
    height = board.size[1] * square_size
    screen_size = (width, height)
    
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    
    tiles = {
        'red': pygame.image.load('viewer_ng/res/red_%s.png' % square_size).convert(),
        'green': pygame.image.load('viewer_ng/res/green_%s.png' % square_size).convert(),
        'entrance': pygame.image.load('viewer_ng/res/entrance_%s.png' % square_size).convert(),
        'exit': pygame.image.load('viewer_ng/res/exit_%s.png' % square_size).convert(),
        'street': pygame.image.load('viewer_ng/res/street_%s.png' % square_size).convert(),
        'oob': pygame.image.load('viewer_ng/res/oob_%s.png' % square_size).convert(),
        'car': pygame.image.load('viewer_ng/res/car_%s.png' % square_size).convert(),
        'special_car': pygame.image.load('viewer_ng/res/special_car_%s.png' % square_size).convert(),
        'intersection': pygame.image.load('viewer_ng/res/intersection_%s.png' % square_size).convert(),
    }
    
    elapsed = 0
    run = False
    done = False
    
    board.draw(screen, tiles)
    pygame.display.flip()
    
    def update():
        tca.update()
        board.update()
        board.draw(screen, tiles)
        
    
    while done == False:
        
        elapsed += clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                done = True
            if event.type == locals.KEYDOWN:
                if event.key == locals.K_SPACE:
                    run = not run
            if event.type == locals.KEYUP:
                if event.key == locals.K_q:
                    done = True
                elif event.key == locals.K_n:
                    run = False
                    update()
        
        if run and elapsed >= 1000 / speed:
            elapsed = 0
            update()
            
        pygame.display.set_caption('%s' % tca.generation)
        pygame.display.flip()
    
    pygame.quit()
    
def start_viewer(topology, square_size=16, speed=10):
    pygame.init()
    
    tca = models.Automaton()
    tca.topology = topology
    topology.automaton = tca
    board = Board(tca)
    
    info = pygame.display.Info()
    
    square_size = min(
        square_size, 
        info.current_w // board.size[0], 
        info.current_h // board.size[1]
    )
    
    width = board.size[0] * square_size
    height = board.size[1] * square_size
    screen_size = (width, height)
    
    create_tiles(square_size)
    
    board.square_size = square_size
    
    screen = pygame.display.set_mode(screen_size, locals.FULLSCREEN | locals.NOFRAME)
    clock = pygame.time.Clock()
    
    tiles = {
        'red': pygame.image.load('viewer_ng/res/red_%s.png' % square_size).convert(),
        'green': pygame.image.load('viewer_ng/res/green_%s.png' % square_size).convert(),
        'entrance': pygame.image.load('viewer_ng/res/entrance_%s.png' % square_size).convert(),
        'exit': pygame.image.load('viewer_ng/res/exit_%s.png' % square_size).convert(),
        'street': pygame.image.load('viewer_ng/res/street_%s.png' % square_size).convert(),
        'oob': pygame.image.load('viewer_ng/res/oob_%s.png' % square_size).convert(),
        'car': pygame.image.load('viewer_ng/res/car_%s.png' % square_size).convert(),
        'special_car': pygame.image.load('viewer_ng/res/special_car_%s.png' % square_size).convert(),
        'intersection': pygame.image.load('viewer_ng/res/intersection_%s.png' % square_size).convert(),
    }
    
    elapsed = 0
    run = False
    done = False
    
    board.draw(screen, tiles)
    pygame.display.flip()
    
    def update():
        tca.update()
        board.update()
        board.draw(screen, tiles)
        
    while done == False:
        elapsed += clock.tick(60)
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                done = True
            if event.type == locals.KEYDOWN:
                if event.key == locals.K_SPACE:
                    run = not run
            if event.type == locals.KEYUP:
                if event.key == locals.K_q:
                    done = True
                elif event.key == locals.K_n:
                    run = False
                    update()
        
        if run and elapsed >= 1000 / speed:
            elapsed = 0
            update()
            
        pygame.display.set_caption('%s' % tca.generation)
        pygame.display.flip()
    
    pygame.quit()