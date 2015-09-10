
from server.tca_parser import parse
from server.tca_renderer import GridMapRenderer
from server.tca.map import TCAMap
from server.tca.automaton import TCAAutomaton


class TCAService(object):

    @staticmethod
    def fixed_time_start(self, cycle_count=60):
        matrix = parse('totito')
        tca_map = TCAMap(matrix)
        self.automaton = TCAAutomaton(tca_map)
        #self.render = GridMapRenderer(map)
        #self.render.get_matrix()

        for i in range(cycle_count):
            self.automaton.update()

        return True

    def dynamic_time_start(self):
        raise NotImplementedError

    def get_traffic_lights(self):
        raise NotImplementedError

    def get_average_speed(self):
        raise NotImplementedError

    def get_average_distance(self):
        raise NotImplementedError

    def get_stopped_time(self):
        raise NotImplementedError
