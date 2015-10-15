import pygame
import random
from viewer_ng.image_creator import create_tiles
from tca_ng import cells, models, example_maps
from pygame import locals


# number of iterations per second
speed = 10
# size of squares in pixels
square_size = 16

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
    else:
        color = 'oob'
        
    if isinstance(cell, cells.Cell):
        if cell.car is not None:
            color = 'special_car' if cell.car.id % 10 == 0 else 'car'
            
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
                cell.absolute_location(square_size)
            )

def test():
    create_tiles(square_size)
    pygame.init()
    
    tca = models.Automaton()
#    topo = example_maps.generate_wide_street(60, 4)
    topo = example_maps.simple_2lane_map()
    tca.topology = topo
    topo.automaton = tca
    board = Board(tca)
    
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
            
        pygame.display.flip()
    
pygame.quit()