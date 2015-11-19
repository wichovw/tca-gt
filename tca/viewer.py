import pygame, pygame.locals as pg_locals
import glob
from PIL import Image
from tca import base

colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'entrance': (0xbb, 0x99, 0xbb),
    'exit': (0xff, 0xbb, 0x33),
    'street': (255, 255, 255),
    'oob': (0x33, 0x33, 0x33),
    'car': (0x99, 0xcc, 0x99),
    'special_car': (0x55, 0x55, 0x99),
    'intersection': (0x99, 0x99, 0x99),
}

def get_color(cell):
    if isinstance(cell, base.StreetCell):
        color = 'street'
    elif isinstance(cell, base.IntersectionCell):
        color = 'intersection'
    elif isinstance(cell, base.Light):
        color = 'green' if cell.free else 'red'
    else:
        color = 'oob'
        
    if isinstance(cell, base.Cell):
        if cell.car is not None:
            color = 'special_car' if cell.car.id % 10 == 0 else 'car'
            
    return color

def create_tiles(size):
    # if tile size already exists, do nothing
    if len(glob.glob('tca/res/*_%s.png' % size)) > 0:
        return True
        
    print('Generating %sx%s tiles...' % (size, size))
        
    for name, color in colors.items():
        tile = Image.new('RGB', (size, size), color=color)
        tile.save('tca/res/%s_%s.png' % (name, size))
        
    return True

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

def start(automaton, square_size=16, speed=10):
    pygame.init()
    board = Board(automaton)
    
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
    
    screen = pygame.display.set_mode(
        screen_size, 
        pg_locals.FULLSCREEN | pg_locals.NOFRAME
    )
    clock = pygame.time.Clock()
    
    res_route = 'tca/res/%s_%s.png'
    tiles = {}
    for color in colors:
        tiles[color] = pygame.image.load(res_route % (color, square_size)).convert()
        
    elapsed = 0
    run = False
    done = False
    
    board.draw(screen, tiles)
    pygame.display.flip()
    
    def update():
        automaton.update()
        board.update()
        board.draw(screen, tiles)
        
    while done == False:
        elapsed += clock.tick(60)
        for event in pygame.event.get():
            if event.type == pg_locals.QUIT:
                done = True
            if event.type == pg_locals.KEYDOWN:
                if event.key == pg_locals.K_SPACE:
                    run = not run
            if event.type == pg_locals.KEYUP:
                if event.key == pg_locals.K_q:
                    done = True
                elif event.key == pg_locals.K_n:
                    run = False
                    update()
        
        if run and elapsed >= 1000 / speed:
            elapsed = 0
            update()
            
        pygame.display.set_caption('%s' % automaton.generation)
        pygame.display.flip()
    
    pygame.quit()