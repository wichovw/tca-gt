from service.tca_service import TCAService


def run():
    # Object
    service = TCAService()

    # Get traffic lights
    print()
    print('Traffic lights dictionary:')
    print(service.get_traffic_lights())
    print()

    # Start running fixed time
    # service.fixed_time_start(10)
    # service.random_fixed_time_start(10)
    service.random_dynamic_time_start(10)


    # # Get average speed
    # print('Average speed: {}'.format(service.get_average_speed()))
    #
    # # Get average cars number
    # print('Average cars number: {}'.format(service.get_average_cars_number()))
    #
    # # Get stopped time
    # print('Total stopped time: {}'.format(service.get_stopped_time()))
    #
    # # Get average stopped time
    # print('Average stopped time: {}'.format(service.get_average_stopped_time()))
    #
    # # Set traffic lights
    # time = []
    # time_1 = dict()
    # time_1['id'] = 0
    # sc_1 = dict()
    # sc_1[0] = 0
    # sc_1[5] = 1
    # time_1['schedule'] = sc_1
    # time.append(time_1)
    # time_2 = dict()
    # time_2['id'] = 1
    # sc_2 = dict()
    # sc_2[0] = 2
    # sc_2[4] = 3
    # time_2['schedule'] = sc_2
    # time.append(time_2)
    # service.set_traffic_lights(time)
    #
    # # Get traffic lights
    # print()
    # print('Traffic lights dictionary:')
    # print(service.get_traffic_lights())
    # print()
    #
    # # Reset statistics
    # print('Reset statistics:')
    # service.reset_statistics()
    #
    # # Get average speed
    # print('Average speed: {}'.format(service.get_average_speed()))
    #
    # # Get average cars number
    # print('Average cars number: {}'.format(service.get_average_cars_number()))
    #
    # # Get stopped time
    # print('Total stopped time: {}'.format(service.get_stopped_time()))
    #
    # # Get average stopped time
    # print('Average stopped time: {}'.format(service.get_average_stopped_time()))
    #
    # # Get intersections
    # print()
    # print('Intersections dictionary:')
    # print(service.get_intersections())
    # print()
    #
    # # Run dynamic time iteration
    # print('Dinamic update result:')
    # print(service.dynamic_time_update())
    # print()

if __name__ == '__main__':
    run()

