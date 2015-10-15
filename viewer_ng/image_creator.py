from PIL import Image
import glob

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
    
def create_tiles(size):
    # if tile size already exists, do nothing
    if len(glob.glob('viewer_ng/res/*_%s.png' % size)) > 0:
        return True
        
    print('Generating %sx%s tiles...' % (size, size))
        
    for name, color in colors.items():
        tile = Image.new('RGB', (size, size), color=color)
        tile.save('viewer_ng/res/%s_%s.png' % (name, size))
        
    return True
    
if __name__ == '__main__':
    create_tiles(16)