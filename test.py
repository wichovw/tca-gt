from service.tca_service import TCAService


def run():
    # Object
    service = TCAService()

    # Get traffic lights
    print()
    print('Traffic lights dictionary:')
    print(service.get_traffic_lights())
    print()

    # Start running
    service.fixed_time_start(10)

    # Get average speed
    print('Average speed: {}'.format(service.get_average_speed()))

    # Get average cars number
    print('Average cars number: {}'.format(service.get_average_cars_number()))

    # Get stopped time
    print('Total stopped time: {}'.format(service.get_stopped_time()))

    # Get average stopped time
    print('Total stopped time: {}'.format(service.get_average_stopped_time()))

    # Set traffic lights
    time = []
    time_1 = dict()
    time_1['id'] = 0
    time_1['time'] = 100
    time.append(time_1)
    time_2 = dict()
    time_2['id'] = 1
    time_2['time'] = 150
    time.append(time_2)
    service.set_traffic_lights(time)

    # Get traffic lights
    print()
    print('Traffic lights dictionary:')
    print(service.get_traffic_lights())
    print()

if __name__ == '__main__':
    run()

