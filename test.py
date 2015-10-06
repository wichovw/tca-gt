from service.tca_service import TCAService


def run():
    # Object
    service = TCAService()

    # Get traffic lights
    print(service.get_traffic_lights())

    # Start running
    service.fixed_time_start(10)

    # Get average speed
    print(service.get_average_speed())

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
    print(service.get_traffic_lights())

    # Get stopped time
    # print(service.get_stopped_time())

if __name__ == '__main__':
    run()

