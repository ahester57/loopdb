import falcon


class LoopResource(object):

    def __init__(self, redis):
        self._redis = redis

    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            resp.status = falcon.HTTP_200
            resp.media = {'status': 'bad'}
            result = self._redis.get(req.params['key'])
            #print(result)
            if (result is None):
                resp.status = falcon.HTTP_404
                resp.media.update({'message': 'key not found'})
            else:
                resp.media.update({'status': 'ok', 'message': result.decode("utf-8")})
        except Exception as e:
            resp.status = falcon.HTTP_500
            print(e)
            resp.media.update({'message': str(e)})
        finally:
            try:
                print(f"response: {resp.media['status']}")
            except:
                print('not sure what went wrong there')

    def on_post(self, req, resp):
        """Handles POST requests"""
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
            print(resp.media)

