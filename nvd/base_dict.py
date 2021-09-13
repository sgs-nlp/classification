import redis
import pickle
from nvd.hasher import string_hash
from django.conf import settings


# class BaseDict:
#     def __init__(self):
#         self.redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)
#
#     def set_item(self, key, value):
#         value = pickle.dumps(value)
#         key = string_hash(str(key))
#         self.redis_instance.set(key, value)
#
#     def get_item(self, key):
#         key = string_hash(str(key))
#         value = self.redis_instance.get(key)
#         if value is not None:
#             value = pickle.loads(value)
#         return value

class BaseDict:

    def set_item(self, key, value):
        value = pickle.dumps(value)
        key = string_hash(str(key))
        settings.CASH_DICTIONARY[key] = value

    def get_item(self, key):
        key = string_hash(str(key))
        if key in settings.CASH_DICTIONARY.items():
            value = pickle.loads(settings.CASH_DICTIONARY[key])
        else:
            value = None
        return value
