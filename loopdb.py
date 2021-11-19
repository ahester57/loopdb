import falcon
import redis
import signal
import sys
import threading
import time

from wsgiref.simple_server import make_server
from redis_connector import redis_connector


class LoopResource(object):

    def __init__(self, redis):
        self._redis = redis

    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            resp.status = falcon.HTTP_200
            result = self._redis.get(req.params['key'])
            #print(result)
            if (result is None):
                resp.status = falcon.HTTP_404
                resp.media = {'status': 'bad', 'message': 'key not found'}
            else:
                resp.media = {'status': 'ok', 'message': str(result)}
        except Exception as e:
            resp.status = falcon.HTTP_500
            print(e)
            resp.media = {'status': 'bad', 'message': str(e)}
        finally:
            print(f"response: {resp.media['status']}")

    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            resp.status = falcon.HTTP_200
            body = req.get_media()
            #print(body)
            key = body['key']
            val = body['value']
            if (key is None):
                resp.status = falcon.HTTP_400
                resp.media = {'status': 'bad', 'message': 'key cannot be null'}
            else:
                self._redis.mset({key: val})
                resp.media = {'status':'ok', 'message': f'{key} added to storage'}
        except Exception as e:
            resp.status = falcon.HTTP_500
            print(e)
            resp.media = {'status': 'bad', 'message': str(e)}
        finally:
            print(resp.media)


print(redis_connector)
redis = redis_connector.RedisConnector.connect()
app = falcon.App()
loop = LoopResource(redis)

app.add_route('/loop', loop)


class LoopServer(threading.Thread):

    def __init__(self, wsgi_app, host='127.0.0.1', port=8080):
        super().__init__()
        self._server = make_server(host, port, wsgi_app)
        self.daemon = True

    def run(self):
        self._server.serve_forever(poll_interval=0.5)

    def stop(self):
        print('exiting')
        self._server.shutdown()
        self.join()


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

