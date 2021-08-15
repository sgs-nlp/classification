import redis
import pickle


class BaseDict:
    def __init__(self):
        self.redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set_item(self, key, value):
        value = pickle.dumps(value)
        self.redis_instance.set(str(key), value)

    def get_item(self, key):
        value = self.redis_instance.get(str(key))
        if value is not None:
            value = pickle.loads(value)
        return value
