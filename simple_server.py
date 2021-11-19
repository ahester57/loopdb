import threading

from wsgiref.simple_server import make_server


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
