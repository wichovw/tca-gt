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
    # Get stopped time
    print(service.get_stopped_time())

if __name__ == '__main__':
    run()
