import falcon
import hiredis
import sys

class LoopResource(object):

    def __init__(self, redis):
        self._redis = redis
        self._reader = hiredis.Reader()

    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            resp.status = falcon.HTTP_200
            resp.media = {'status': 'bad'}
            result_buffer = self._redis.get(req.params['key'])
            self._reader.feed(result_buffer.decode('utf-8'))
            result = ''
            while not self._reader.has_data():
                pass
            print('getting result')
            result = self._reader.gets()

            #print(result)
            if (result is None):
                resp.status = falcon.HTTP_404
                resp.media.update({'message': 'key not found'})
            else:
                resp.media.update({'status': 'ok', 'message': result})
        except Exception as e:
            resp.status = falcon.HTTP_500
            print(e)
            resp.media.update({'message': str(e)})
        finally:
            # https://stackoverflow.com/a/11489429/7032978
            sys.stderr.close()
            try:
                print(f"response: {resp.media['status']}")
            except:
                print('not sure what went wrong there')

    def on_post(self, req, resp):
        """Handles POST requests"""
        print('loop.on_post', req)
        try:
            resp.status = falcon.HTTP_200
            resp.media = {'status': 'bad'}
            body = req.get_media()
            #print(body)
            key = body['key']
            val = body['value']
            if (key is None):
                resp.status = falcon.HTTP_400
                resp.media.update({'message': 'key cannot be null'})
            else:
                self._redis.mset({key: val})
                resp.media.update({'status':'ok', 'message': f'{key} added to storage'})
        except Exception as e:
            resp.status = falcon.HTTP_500
            print(e)
            resp.media.update({'message': str(e)})
        finally:
            # https://stackoverflow.com/a/11489429/7032978
            sys.stderr.close()
            print(resp.media)

