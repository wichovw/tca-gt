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

    def dynamic_time_start(self):
        raise NotImplementedError

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