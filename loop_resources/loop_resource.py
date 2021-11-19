import falcon


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

