import pygame, pygame.locals as pg_locals
import glob
import random
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

def get_color(cell, selected_car):
    if isinstance(cell, base.StreetCell):
        color = 'street'
    elif isinstance(cell, base.IntersectionCell):
        color = 'intersection'
        if selected_car is not None and selected_car.route is not None:
            if cell in selected_car.route.cells:
                color = 'entrance'
    elif isinstance(cell, base.Light):
        color = 'green' if cell.free else 'red'
    else:
        color = 'oob'
        
    if isinstance(cell, base.Cell):
        if cell.car is not None:
            color = 'special_car' if cell.car == selected_car else 'car'     
            
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
    selected_car = None
    
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
            cell.color = get_color(aut_cell, self.selected_car)
            self.cells.append(cell)
            return max_x, max_y
            
        for aut_cell in self.automaton.topology.cells:
            max_x, max_y = map_(aut_cell, max_x, max_y)
        for light in self.automaton.topology.lights:
            max_x, max_y = map_(light, max_x, max_y)
        self.size = (max_x, max_y)
        
    def update(self):
        for cell in self.cells:
            cell.color = get_color(cell.aut_cell, self.selected_car)
            
    def draw(self, screen, tiles):
        for cell in self.cells:
            screen.blit(
                tiles[cell.color],
                cell.absolute_location(self.square_size)
            )

def start(automaton, square_size=16, speed=10):
    pygame.init()
    board = Board(automaton)
    
    panel_width = 300
    
    info = pygame.display.Info()
    square_size = min(
        square_size, 
        (info.current_w - panel_width) // board.size[0], 
        info.current_h // board.size[1]
    )
    
    width = board.size[0] * square_size + panel_width
    height = board.size[1] * square_size
    screen_size = (width, height)
    panel_start_x = width - panel_width + 25
    
    create_tiles(square_size)
    
    board.square_size = square_size
    
    screen = pygame.display.set_mode(
        screen_size, 
        pg_locals.FULLSCREEN | pg_locals.NOFRAME
    )
    clock = pygame.time.Clock()
    
    title_font = pygame.font.SysFont("sansserif", 32)
    data_font = pygame.font.SysFont("sansserif", 24)
    
    res_route = 'tca/res/%s_%s.png'
    tiles = {}
    for color in colors:
        tiles[color] = pygame.image.load(res_route % (color, square_size)).convert()
        
    elapsed = 0
    run = False
    done = False
    
    label = title_font.render("Traffic Simulator", 1, (255, 255, 255))
    screen.blit(label, (panel_start_x, 25))
    
    board.draw(screen, tiles)
    pygame.display.flip()
    
    def update():
        automaton.update()
        board.update()
        board.draw(screen, tiles)
        
        cars = [c.car for c in automaton.topology.cells if c.car is not None]
        m_cars = [c for c in cars if c.speed > 0]
        factor = 10.38461538
        if board.selected_car not in cars:
            board.selected_car = random.choice(cars)
        
        generations = data_font.render(
            "TCA generations: %s (%.1f min)   " % (automaton.generation, automaton.generation*2.6/60),
            1, (255, 255, 255), (0, 0, 0))
        
        no_of_cars = data_font.render(
            "Total number of cars: %s   " % len(cars),
            1, (255, 255, 255), (0, 0, 0))
        avg_speed = data_font.render(
            "Average speed: %.2f cells / iter   " % (sum(c.speed for c in cars) / max(1, len(cars))),
            1, (255, 255, 255), (0, 0, 0))
        avg_speed_units = data_font.render(
            "Average speed: %.2f km / h   " % (sum(c.speed for c in cars) / max(1, len(cars)) * factor),
            1, (255, 255, 255), (0, 0, 0))
        
        m_no_of_cars = data_font.render(
            "Number of cars in movement: %s   " % len(m_cars),
            1, (255, 255, 255), (0, 0, 0))
        m_avg_speed = data_font.render(
            "Average speed: %.2f cells / iter   " % (sum(c.speed for c in m_cars) / max(1, len(m_cars))),
            1, (255, 255, 255), (0, 0, 0))
        m_avg_speed_units = data_font.render(
            "Average speed: %.2f km / h   " % (sum(c.speed for c in m_cars) / max(1, len(m_cars)) * factor),
            1, (255, 255, 255), (0, 0, 0))
        
        car_id = data_font.render(
            "Selected car id: %s   " % board.selected_car.id,
            1, (255, 255, 255), (0, 0, 0))
        car_speed = data_font.render(
            "Car speed: %s cells / iter   " % board.selected_car.speed,
            1, (255, 255, 255), (0, 0, 0))
        car_speed_units = data_font.render(
            "Car speed: %.2f km / h   " % (board.selected_car.speed * factor),
            1, (255, 255, 255), (0, 0, 0))
        car_change = data_font.render(
            "Lane change prob.: %.2f   " % board.selected_car.lane_changing_rate,
            1, (255, 255, 255), (0, 0, 0))
        
        wildcard = data_font.render(
            "dest density: %s   " % board.selected_car.dest_street.get_density() if board.selected_car.dest_street is not None else "-",
            1, (255, 255, 255), (0, 0, 0))
        
        line = 0
        screen.blit(generations, (panel_start_x, 70 + (line)*30)); line += 1
        line += 1
        screen.blit(no_of_cars, (panel_start_x, 70 + (line)*30)); line += 1
        screen.blit(avg_speed, (panel_start_x, 70 + (line)*30)); line += 1
        screen.blit(avg_speed_units, (panel_start_x, 70 + (line)*30)); line += 1
        line += 1
        screen.blit(m_no_of_cars, (panel_start_x, 70 + (line)*30)); line += 1
        screen.blit(m_avg_speed, (panel_start_x, 70 + (line)*30)); line += 1
        screen.blit(m_avg_speed_units, (panel_start_x, 70 + (line)*30)); line += 1
        line += 1
        screen.blit(car_id, (panel_start_x, 70 + (line)*30)); line += 1
        screen.blit(car_speed, (panel_start_x, 70 + (line)*30)); line += 1
        screen.blit(car_speed_units, (panel_start_x, 70 + (line)*30)); line += 1
        screen.blit(car_change, (panel_start_x, 70 + (line)*30)); line += 1
        line += 1
        screen.blit(wildcard, (panel_start_x, 70 + (line)*30)); line += 1
        
    while done == False:
        elapsed += clock.tick(60)
        for event in pygame.event.get():
            if event.type == pg_locals.QUIT:
                done = True
            if event.type == pg_locals.KEYDOWN:
                if event.key == pg_locals.K_SPACE:
                    run = not run
            if event.type == pg_locals.KEYUP:
                if event.key == pg_locals.K_q or event.key == pg_locals.K_ESCAPE:
                    done = True
                elif event.key == pg_locals.K_n:
                    run = False
                    update()
                elif event.key == pg_locals.K_UP:
                    speed *= 1.5
                elif event.key == pg_locals.K_DOWN:
                    speed /= 1.5
        
        if run and elapsed >= 1000 / speed:
            elapsed = 0
            update()
            
        pygame.display.set_caption('%s' % automaton.generation)
        pygame.display.flip()
    
    pygame.quit()