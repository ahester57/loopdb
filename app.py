import falcon
import signal
import sys
import time

from loopresources import LoopResource, DupeResource
from redisconnector import RedisConnector
from simple_server import LoopServer


class App(object):
    def __init__(self):
        self._redis_instance = RedisConnector()
        self._falcon_app = falcon.App()
        self.create_resources()
        self.create_routes()
        self.create_server()

    def create_resources(self):
        self._loop = LoopResource(self._redis_instance)
        self._dupe = DupeResource()

    def create_routes(self):
        self._falcon_app.add_route('/loop', self._loop)
        self._falcon_app.add_route('/dupe', self._dupe)

    def create_server(self):
        self._loop_server = LoopServer(self.get_falcon_app())

    def get_falcon_app(self):
        return self._falcon_app

    def start_server(self):
        self._loop_server.start()

    def stop_server(self):
        self._loop_server.stop()

    def __repr__(self):
        return f'''
Redis: {self._redis_instance}
Falcon: {self._falcon_app}
Server: {self._loop_server}
'''


if __name__ == '__main__':

    app = App()

    def signal_handler(signal_num=None, frame=None):
        print('looping out')
        app.stop_server()
        sys.exit(1)

    # Set the app to handle interrupt signal with our custom signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print(f'\nboutta serve: {app}')
    app.start_server()
    print(f'Serving: {app}')

    # wait here for CLI inputs
    try:
        while True:
            time.sleep(1)
    except:
        print('looping out on accident')
        app.stop_server()
