from service.tca_service import TCAService


def run():
    service = TCAService()
    service.start()

    for i in range(100):
        service.update()

if __name__ == '__main__':
    run()
