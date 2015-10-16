from tca_ng.models import Automaton
from tca_ng.example_maps import totito_map, grid_2lane_map
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

    def __init__(self, map = 1):
        """
        TCAService __init__
        :return:
        """
        # Automaton
        self._automaton = Automaton()
        if map == 1:
            self._automaton.topology = totito_map(10)
        elif map == 2:
            self._automaton.topology = grid_2lane_map()
        self._automaton.topology.automaton = self._automaton

        # Class attributes
        self.traffic_lights = []
        self.average_speed = None
        self.step_average_speed = []
        # self.average_distance = 0
        self.stopped_time = 0
        self.step_stopped_time = []
        self.average_stopped_time = 0
        # self.stopped_time_per_car
        self.average_cars_number = None
        self.step_car_number = []
        self._cycle_count = 0
        self.intersections = []
        self.streets = []
        self.iteration = 0

        # Build data from map
        self._build_traffic_lights()
        self._build_intersections()

    def fixed_time_start(self, cycle_count=60, all_data=False):
        """
        Simulation start using a fixed time strategy
        :param cycle_count: Number of cycles to be simulated
        :param all_data: If True print data to file
        :return: True if simulation was successfully completed
        """

        # Set simulation values
        self._cycle_count = cycle_count

        try:

            # Simulate and get data from TCA simulator
            for i in range(cycle_count):
                self._automaton.update()
                self.iteration += 1
                self._update_data()

            # Process obtained data
            self._process_data()

            # Print obtained data to file
            if all_data:
                self._print_data()

        except Exception as e:
            print('\nERROR: Simulator raised an exception!')
            print('Exception message: {} \n'.format(e))
            return False

        # Success
        return True

    def dynamic_time_update(self, cycle_count=5, all_data=False):
        """
        Simulation update using dynamic time strategy
        :param cycle_count: Number of updates to be simulated
        :param all_data: If True print data to file
        :return: List containing streets information in this format

            [
                {'id': 0, 'cars_number': 9, 'average_speed': 2.5},
                {'id': 1, 'cars_number': 11, 'average_speed': 3.1},
                {'id': 2, 'cars_number': 9, 'average_speed': 2.3}
            ]

        """

        try:

            # Simulate and get data from TCA simulator
            for i in range(cycle_count):
                self._automaton.update()
                self.iteration += 1
                self._update_data()

            # Process obtained data
            self._process_data()

            # Print obtained data to file
            if all_data:
                self._print_data()

        except Exception as e:
            print('\nERROR: Simulator raised an exception!')
            print('Exception message: {} \n'.format(e))
            return None

        # Success, build and return data
        self._build_streets()
        return self.streets

    def random_fixed_time_start(self, cycle_count=60, min_time=5, max_time=20, all_data=False):
        raise NotImplementedError

    def random_dynamic_time_start(self, cycle_count=60, variation_time=5, all_data=False):
        raise NotImplementedError

    def reset_statistics(self):
        """
        Reset statistics to zero or empty
        :return:
        """

        self.average_speed = 0
        self.step_average_speed = []
        self.stopped_time = 0
        self.step_stopped_time = []
        self.average_stopped_time = 0
        self.average_cars_number = 0
        self.step_car_number = []
        self._cycle_count = 0
        self.iteration = 0

    def get_actual_iteration(self):
        """
        Get actual iteration number
        :return: iteration number
        """

        return self.iteration

    def get_max_speed(self):
        """
        Get max speed car speed in simulator
        :return: max speed
        """

        # TODO get real value
        return 3

    def get_intersections(self):
        """
        Get intersections in this format:

            [
                {'id': 0, 'traffic_light': 0, 'in_streets': [0, 1], 'out_streets': [2, 3]},
                {'id': 1, 'traffic_light': 1, 'in_streets': [3, 4], 'out_streets': [5, 6]},
                {'id': 2, 'traffic_light': 2, 'in_streets': [6, 2], 'out_streets': [0, 4]}
            ]

        :return: List containing dictionaries representing intersections
        """

        return self.intersections

    def get_extended_intersections(self):
        raise NotImplementedError

    def get_traffic_lights(self):
        """
        Get traffic lights in this format:

            [
                {'id': 0, 'schedule': {0: 0, 5: 1}, 'lights': [0, 1]},
                {'id': 1, 'schedule': {0: 2, 4: 3}, 'lights': [2, 3]},
                {'id': 2, 'schedule': {2: 4, 6: 5}, 'lights': [4, 5]}
            ]

        :return: List containing dictionaries representing traffic lights
        """
        # Re build traffic lights
        self._build_traffic_lights()

        # Return dictionary containing traffic lights information
        return self.traffic_lights

    def set_traffic_lights(self, traffic_light_schedule):
        """
        Set traffic lights schedule:

            [
                {'id': 0, 'schedule': {0: 0, 5: 1},
                {'id': 1, 'schedule': {0: 2, 4: 3},
                {'id': 2, 'schedule': {2: 4, 6: 5}
            ]
        :param traffic_light_schedule: Dictionary containing traffic lights schedule
        :return: True if traffic lights schedule changed correctly
        """
        try:
            for schedule in traffic_light_schedule:
                traffic_light = self._search_traffic_light(schedule['id'])

                # Build and set new schedule dictionary to change format
                new_schedule = dict()
                for offset, light in schedule['schedule'].items():
                    new_schedule[offset] = self._search_light(light)

                traffic_light.set_schedule(new_schedule)

        except InvalidTrafficLightId as invalid_traffic_light_id:
            raise invalid_traffic_light_id
        except InvalidLightId as invalid_light_id:
            raise invalid_light_id
        except Exception as e:
            print('\nERROR: Incorrect dictionary for setting traffic lights schedule!')
            print('Exception message: {} \n'.format(e))
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

    def get_average_stopped_time(self):
        """
        Get average stopped time

        Formula:
            (stopped_time_iteration_1 + stopped_time_iteration_2 + stopped_time_iteration_number_of_cycles) / number_of_cycles
        :return: Average stopped time, None if not available
        """

        return self.average_stopped_time

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

    def _search_traffic_light(self, traffic_light_id):
        """
        Search for a traffic light into semaphore list
        :param id: id of the traffic light
        :return: traffic light object, None if doesn't exists
        """
        for traffic_light in self._automaton.topology.semaphores:
            if traffic_light.id == traffic_light_id:
                return traffic_light

        # Raise exception if id doesn't exists
        raise InvalidTrafficLightId(traffic_light_id)

    def _search_light(self, light_id):
        """
        Search for a light into light list
        :param light_id: id of the light
        :return: light object, None if doesn't exists
        """

        for light in self._automaton.topology.lights:
            if light.id == light_id:
                return light

        # Raise exception if id doesn't exists
        raise InvalidLightId(light_id)

    def _update_data(self):
        """
        Get data from simulator for metrics
        :return:
        """

        # Stopped time counter
        cycle_stopped_time = 0

        # Update average speed (cumulative speed of all cars / number of cars)
        # Update stopped time, increment 1 when speed equals 0
        cumulative_speed = 0
        for car in self._automaton.topology.cars:
            if car.speed == 0:
                self.stopped_time += 1
                cycle_stopped_time += 1
            cumulative_speed += car.speed

        self.step_average_speed.append(cumulative_speed / len(self._automaton.topology.cars))

        # Update stopped time
        self.step_stopped_time.append(cycle_stopped_time)

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

        # Process average stopped time per simulation
        self.average_stopped_time = sum(self.step_stopped_time) / float(len(self.step_stopped_time))

    def _print_data(self):
        raise NotImplementedError

    def _build_streets(self):
        """
        Build list containing dictionaries representing streets with metrics information
        :return:
        """

        # Clean streets list
        self.streets = []

        for street in self._automaton.topology.streets:

            # Create new dictionary and add street id
            street_dict = dict()
            street_dict['id'] = street.id

            # Data values
            cars_number = 0
            total_speed = 0

            # Iterate cells in streets and get data
            for lane in street.cells:
                for cell in lane:
                    if cell.car is not None:
                        cars_number += 1
                        total_speed += cell.car.speed

            # Add data to dictionary
            if cars_number > 0:
                street_dict['cars_number'] = cars_number
                street_dict['average_speed'] = round(total_speed/cars_number, 2)
            else:
                street_dict['cars_number'] = 0
                street_dict['average_speed'] = 0

            # Add intersection to intersection list
            self.streets.append(street_dict)

    def _build_intersections(self):
        """
        Build list containing dictionaries representing intersections
        :return:
        """

        # Clean intersection list
        self.intersections = []

        # Iterate all intersections in simulator map
        for intersection in self._automaton.topology.intersections:

            # Create new dictionary and add intersection id
            intersection_dict = dict()
            intersection_dict['id'] = intersection.id

            # Add traffic light to intersection dictionary
            intersection_dict['traffic_light'] = intersection.semaphore.id

            # Build in streets and add it to dictionary
            in_streets = []
            for street in intersection.in_streets:
                in_streets.append(street.id)
            intersection_dict['in_streets'] = in_streets

            # Build out streets and add it to dictionary
            out_streets = []
            for street in intersection.out_streets:
                out_streets.append(street.id)
            intersection_dict['out_streets'] = out_streets

            # Build neighbors
            neighbors = []
            for neighbor in intersection.neighbors:
                neighbors.append(neighbor.id)
            intersection_dict['neighbors'] = neighbors

            # Add intersection to intersection list
            self.intersections.append(intersection_dict)

    def _build_traffic_lights(self):
        """
        Build list containing dictionaries representing traffic lights
        :return:
        """

        # Clean traffic lights list
        self.traffic_lights = []

        # Iterate all traffic lights in simulator map
        for traffic_light in self._automaton.topology.semaphores:

            # Create new dictionary and add traffic_light id
            traffic_light_dict = dict()
            traffic_light_dict['id'] = traffic_light.id

            # Build lights list and add it to dictionary
            lights = []
            for light in traffic_light.lights:
                lights.append(light.id)
            traffic_light_dict['lights'] = lights

            # Build schedule and add it to dictionary
            schedule = dict()
            for start, value in traffic_light.schedule.items():
                schedule[start] = value['light'].id
            # Add traffic_light schedule
            traffic_light_dict['schedule'] = schedule

            # Add traffic_light dictionary to traffic lights list
            self.traffic_lights.append(traffic_light_dict)


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


class InvalidLightId(Exception):
    """
    Custom exception to raise when a light id is not found.
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
        return 'Error: The light id ({}) does not exists in simulator!'.format(repr(self.value))

