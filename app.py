import falcon
import os
import signal
import sys
import time

from loopresources import LoopResource, DupeResource
from redisconnector import RedisConnector
from simple_server import LoopServer


class App(object):
    def __init__(self, redis_host='localhost', redis_port=6379, falcon_host='localhost', falcon_port=8080):
        # setup Redis
        if (os.environ.get('LOOP_REDIS_HOST') is not None):
            self._redis_host = os.environ.get('LOOP_REDIS_HOST')
        else:
            self._redis_host = redis_host
        if (os.environ.get('LOOP_REDIS_PORT') is not None):
            self._redis_port = os.environ.get('LOOP_REDIS_PORT')
        else:
            self._redis_port = redis_port
        self._redis_instance = RedisConnector(self._redis_host, self._redis_port)

        # setup Falcon
        self.create_resources()
        self._falcon_app = falcon.App()
        self.create_routes()

        # setup Server
        if (os.environ.get('LOOP_FALCON_HOST') is not None):
            self._falcon_host = os.environ.get('LOOP_FALCON_HOST')
        else:
            self._falcon_host = falcon_host
        if (os.environ.get('LOOP_FALCON_PORT') is not None):
            self._falcon_port = os.environ.get('LOOP_FALCON_PORT')
        else:
            self._falcon_port = falcon_port
        self.create_server()

    def create_resources(self):
        self._loop = LoopResource(self._redis_instance)
        self._dupe = DupeResource()

    def create_routes(self):
        self._falcon_app.add_route('/loop', self._loop)
        self._falcon_app.add_route('/dupe', self._dupe)

    def create_server(self):
        self._loop_server = LoopServer(self.get_falcon_app(), self._falcon_host, self._falcon_port)

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
