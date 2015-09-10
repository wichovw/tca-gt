
from server.tca_parser import parse
from server.tca_renderer import GridMapRenderer
from server.tca.map import TCAMap
from server.tca.automaton import TCAAutomaton



class TCAService(object):

    def start(self, size=2):
        #        matrix = create_map(rows, cols)
        matrix = parse('totito')
        map = TCAMap(matrix)
        self.automaton = TCAAutomaton(map)
        self.render = GridMapRenderer(map)
        return self.render.get_matrix()

    def update(self):
        self.automaton.update()
        return self.render.get_matrix()
