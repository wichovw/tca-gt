from tca_ng.models import Automaton
from tca_ng.example_maps import totito_map
import random


class TCAService(object):
    """
    Traffic Cellular Automaton Service - Application Program Interface for TCA simulator

    Strategies:
        -Fixed traffic lights time
        -Dynamic traffic lights  time

    Metrics:
        -Average cars speed
        -Total stopped time
    """

    def __init__(self):
        """
        TCAService __init__
        :return:
        """
        # Automaton
        self._automaton = Automaton()
        self._automaton.topology = totito_map(10)
        # matrix = parse('totito')
        # tca_map = TCAMap(matrix)
        # self._automaton = TCAAutomaton(tca_map)
        # return self.automaton.topology.json_view()

        # Class attributes
        self.traffic_lights = []
        self.average_speed = 0
        self._cumulative_speed = 0
        self._average_distance = 0
        self.stopped_time = 0
        self._car_number = 0
        self._cycle_count = 0

        # self.render = GridMapRenderer(map)
        # self.render.get_matrix()

        # Populate traffic lights list
        # self._build_traffic_lights(tca_map.semaphores)

    def fixed_time_start(self, cycle_count=60):
        """
        Simulation start using a fixed time strategy
        :param cycle_count: Number of cycles to be simulated
        :return: True if simulation was successfully completed
        """

        # Set simulation values
        self._cycle_count = cycle_count
        # TODO set number of cars into automaton
        self._car_number = 100

        try:

            # Simulate and get data from TCA simulator
            for i in range(cycle_count):
                self._automaton.update()
                # self._get_data()

                print()
                print('total cars', len(self._automaton.topology.cars))
                for car in self._automaton.topology.cars:
                    if car.id % 10 == 0:
                        print('car %3s %8s route: %s' % (
                                car.id,
                                tuple(car.cell.viewer_address),
                                car.route
                        ))

                # modify a light
                light = random.choice(self._automaton.topology.lights)
                change = random.randint(-2, 2)
                print(light, light.time, change)
                light.time += change
                print()

            # Process obtained data
            # self._process_data()

        except Exception:
            return False

        # Success
        return True

    def dynamic_time_start(self):
        raise NotImplementedError

    def get_traffic_lights(self):
        """
        Get traffic lights in this format:

            [
                {'id_1': 10, 'id_2': 5},
                {'id_3': 5, 'id_4': 5},
                {'id_5': 15, 'id_6': 20}
            ]

        :return: List containing dictionaries representing traffic lights
        """
        return self.traffic_lights

    def get_average_speed(self):
        """
        Get average speed of the simulation

        Formula:
            (car_1_speed_1 + car_2_speed_1 + car_1_speed_2 + car_2_speed_2) / number_of_cars / number_of_cycles

        :return: Average speed
        """
        return self.average_speed

    def get_average_distance(self):
        raise NotImplementedError

    def get_stopped_time(self):
        """
        Get stopped time of cars in simulation

        Formula:
            If car speed == 0, stopped time += 1

        :return: Stopped time
        """
        return self.stopped_time

    def _get_data(self):
        """
        Get data from simulator for metrics
        :return:
        """

        # Iterate into map items getting cars data
        for street_id, street in self._automaton.map.streets.items():
            for lane in range(street.width):
                for cell in range(street.height + street.front_offset):
                    car = self._automaton.map.get((street_id, lane, cell))
                    if car:
                        # When we get a car
                        if car.speed != 0:
                            self._cumulative_speed += car.speed
                        else:
                            self.stopped_time += 1

    def _process_data(self):
        """
        Process final data
        :return:
        """

        # Process average speed
        self.average_speed = self._cumulative_speed/self._car_number/self._cycle_count

    def _build_traffic_lights(self, semaphores):
        """
        Build list containing dictionaries representing traffic lights
        :param semaphores: Semaphores of simulator map
        :return:
        """

        # Clean traffic lights list
        self.traffic_lights = []

        # Iterate all semaphores in simulator map
        for semaphore in semaphores:
            s = {}

            # For each light add it to a dictionary {'id': time}
            for light in semaphore.lights:
                s[light.id] = light.time

            # Add dictionary to list
            self.traffic_lights.append(s)
