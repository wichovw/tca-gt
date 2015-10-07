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
        self.average_speed = None
        self.step_average_speed = []
        # self._average_distance = 0
        self.stopped_time = 0
        self.average_cars_number = None
        self.step_car_number = []
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
                #
                # # modify a light
                # light = random.choice(self._automaton.topology.lights)
                # change = random.randint(-2, 2)
                # print(light, light.time, change)
                # light.time += change
                # print()

            # Process obtained data
            self._process_data()

        except:
            print('ERROR: Simulator raised an exception!')
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
        # Re build traffic lights
        self._build_traffic_lights()

        # Return dictionary containing traffic lights information
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
                light.time = time['time']

        except InvalidTrafficLightId as invalid_id:
            raise invalid_id
        except:
            print('ERROR: Incorrect dictionary for setting traffic lights time!')
            return False

        # Success
        return True

    def get_average_speed(self):
        """
        Get average speed of the simulation

        Formula:
            (car_1_speed_1 + car_2_speed_1 + car_1_speed_2 + car_2_speed_2) / number_of_cars / number_of_cycles

        :return: Average speed, None if not available
        """
        return self.average_speed

    def get_average_cars_number(self):
        """
        Get average cars number

        Formula:
            (cars_number_iteration_1 + cars_number_iteration_2 + cars_number_iteration_number_of_cycles) / number_of_cycles
        :return: Average cars number, None if not available
        """

        return self.average_cars_number

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

    def _search_traffic_light(self, light_id):
        """
        Searh for a traffic light into light list
        :param id: id of the traffic light
        :return: light object, None if doesn't exists
        """
        for light in self._automaton.topology.lights:
            if light.id == light_id:
                return light

        # Raise exception if id doesn't exists
        raise InvalidTrafficLightId(light_id)

    def _update_data(self):
        """
        Get data from simulator for metrics
        :return:
        """

        # Update average speed (cumulative speed of all cars / number of cars)
        # Update stopped time, increment 1 when speed equals 0
        cumulative_speed = 0
        for car in self._automaton.topology.cars:
            if car.speed == 0:
                self.stopped_time += 1
            cumulative_speed += car.speed

        self.step_average_speed.append(cumulative_speed / len(self._automaton.topology.cars))

        # Update cars number
        self.step_car_number.append(len(self._automaton.topology.cars))

    def _process_data(self):
        """
        Process final data
        :return:
        """

        # Process average speed
        self.average_speed = sum(self.step_average_speed) / float(len(self.step_average_speed))

        # Process average cars number
        self.average_cars_number = int(round(sum(self.step_car_number) / float(len(self.step_car_number)), 0))

    def _build_traffic_lights(self):
        """
        Build list containing dictionaries representing traffic lights
        :return:
        """

        # Clean traffic lights list
        self.traffic_lights = []

        # Iterate all semaphores in simulator map
        for semaphore in self._automaton.topology.semaphores:

            # Create new dictionary and add semaphore id
            semaphore_dict = dict()
            semaphore_dict['id'] = semaphore.id

            # Build lights list and add it to dictionary
            lights = []
            for light in semaphore.states:
                lights.append(light.id)
            semaphore_dict['lights'] = lights

            # Add semaphore schedule
            semaphore_dict['schedule'] = None

            # Add semaphore dictionary to traffic lights list
            self.traffic_lights.append(semaphore_dict)


class InvalidTrafficLightId(Exception):
    """
    Custom exception to raise when a traffic light id is not found.
    """
    def __init__(self, value):
        """
        Exception __init__
        :param value: Value that is incorrect
        :return:
        """
        self.value = value

    def __str__(self):
        """
        Exception string representation
        :return: Message with error representation
        """
        return 'ERROR: The traffic light id ({}) does not exists in simulator!'.format(repr(self.value))
