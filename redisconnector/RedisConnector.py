import redis


class RedisConnector(object):

    def __init__(self, host='localhost', port=6379):
        self.host = host
        self.port = port
        self._pool = self.connect_to_pool()
        self._redis = self.connect_to_redis()

    def connect_to_pool(self):
        try:
            return redis.ConnectionPool(
                host=self.host,
                port=self.port,
                db=0
            )
        except Exception as e:
            print(f'redis connection-pool failure: {str(e)}')

    def connect_to_redis(self):
        try:
            return redis.Redis(connection_pool=self._pool)
        except Exception as e:
            print(f'redis connection failure: {str(e)}')

    def get(self, key):
        return self._redis.get(key)

    def mset(self, data):
        self._redis.mset(data)
