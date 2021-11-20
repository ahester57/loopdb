import falcon


class DupeResource(object):

    def __init__(self):
        pass

    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            resp.status = falcon.HTTP_200
            resp.media = {'status': 'bad'}
            resp.media.update({'status': 'ok', 'message': 'dupe'})
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
                #self._redis.mset({key: val})
                resp.media.update({'status':'ok', 'message': f'{key} not added to storage'})
        except Exception as e:
            resp.status = falcon.HTTP_500
            print(e)
            resp.media.update({'message': str(e)})
        finally:
            print(resp.media)

