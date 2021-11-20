import falcon
import signal
import sys
import time

from loop_resources import loop_resource, dupe_resource
from redis_connector import redis_connector
from simple_server import LoopServer


print(redis_connector)
redis_instance = redis_connector.RedisConnector()
print(redis_instance)
app = falcon.App()


loop = loop_resource.LoopResource(redis_instance)
dupe = dupe_resource.DupeResource()

app.add_route('/loop', loop)
app.add_route('/dupe', dupe)

if __name__ == '__main__':

    loop_server = LoopServer(app)

    def signal_handler(signal_num=None, frame=None):
        print('looping out')
        loop_server.stop()
        sys.exit(1)

    # Set the app to handle interrupt signal with our custom signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print(f'boutta serve: {loop_server}')
    loop_server.start()
    print(f'Serving: {loop_server}')
    try:
        while True:
            time.sleep(1)
    except:
        print('looping out on accident')
        loop_server.stop()

