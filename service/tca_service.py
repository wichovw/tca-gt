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

        # Class attributes
        self.traffic_lights = []
        self.average_speed = 0
        self.step_average_speed = []
        # self._cumulative_speed = 0
        # self._average_distance = 0
        # self.stopped_time = 0
        # self._car_number = 0
        self._cycle_count = 0

        # Build data from map
        self._build_traffic_lights()

    def fixed_time_start(self, cycle_count=60, all_data=False):
        """
        Simulation start using a fixed time strategy
        :param cycle_count: Number of cycles to be simulated
        :return: True if simulation was successfully completed
        """

        # Set simulation values
        self._cycle_count = cycle_count

        try:

            # Simulate and get data from TCA simulator
            for i in range(cycle_count):
                self._automaton.update()
                self._update_data()

                # print()
                # print('total cars', len(self._automaton.topology.cars))
                # for car in self._automaton.topology.cars:
                #     if car.id % 10 == 0:
                #         print('car %3s %8s route: %s' % (
                #                 car.id,
                #                 tuple(car.cell.viewer_address),
                #                 car.route
                #         ))

                # modify a light
                # light = random.choice(self._automaton.topology.lights)
                # change = random.randint(-2, 2)
                # print(light, light.time, change)
                # light.time += change
                # print()

            # Process obtained data
            self._process_data()

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
                {'id': 0, 'time': 20},
                {'id': 1, 'time': 5},
                {'id': 2, 'time': 15}
            ]

        :return: List containing dictionaries representing traffic lights
        """
        return self.traffic_lights

    def set_traffic_lights(self, traffic_light_time):
        """
        Set traffic lights in this format:

            [
                {'id': 0, 'time': 20},
                {'id': 1, 'time': 5},
                {'id': 2, 'time': 15}
            ]
        :param traffic_light_time: Dictionary containing traffic lights time
        :return: True if traffic lights time changed correctly
        """
        try:
            for time in traffic_light_time:
                light = self._search_traffic_light(time['id'])
                # If light exists
                if not light:
                    light.time = time[time]
                else:
                    raise KeyError

        except Exception:
            return False

        # Success
        return True

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

    def _search_traffic_light(self, id):
        """
        Searh for a traffic light into light list
        :param id: id of the traffic light
        :return: light object, None if doesn't exists
        """
        for light in self._automaton.topology.lights:
            if light.id == id:
                return light

        # None if id doesn't exists
        return None

    def _update_data(self):
        """
        Get data from simulator for metrics
        :return:
        """

        # Update average speed (cumulative speed of all cars / number of cars)
        cumulative_speed = 0
        for car in self._automaton.topology.cars:
            cumulative_speed += car.speed

        self.step_average_speed.append(cumulative_speed / len(self._automaton.topology.cars))

    def _process_data(self):
        """
        Process final data
        :return:
        """

        # Process average speed
        self.average_speed = sum(self.step_average_speed) / float(len(self.step_average_speed))

    def _build_traffic_lights(self):
        """
        Build list containing dictionaries representing traffic lights
        :param semaphores: Semaphores of simulator map
        :return:
        """

        # Clean traffic lights list
        self.traffic_lights = []

        # Iterate all semaphores in simulator map
        for light in self._automaton.topology.lights:
            l = {}
            l['id'] = light.id
            l['time'] = light.time

            # Add dictionary {'id': x, 'time': y} to list
            self.traffic_lights.append(l)
