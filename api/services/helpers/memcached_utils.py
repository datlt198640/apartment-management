import json
from pymemcache.client.base import Client
from django.conf import settings


class JsonSerde(object):
    def serialize(self, key, value):
        if isinstance(value, str):
            return value.encode("utf-8"), 1
        return json.dumps(value, default=str).encode("utf-8"), 2

    def deserialize(self, key, value, flags):
        if flags == 1:
            return value.decode("utf-8")
        if flags == 2:
            return json.loads(value.decode("utf-8"))
        raise Exception("Unknown serialization format")


class MemcachedUtils:
    @staticmethod
    def get_client():
        return Client(
            (settings.MEMCACHED_HOST, settings.MEMCACHED_PORT), serde=JsonSerde()
        )

    @staticmethod
    def get(key):
        client = MemcachedUtils.get_client()
        return client.get(str(key))

    @staticmethod
    def set(key, value):
        client = MemcachedUtils.get_client()
        client.set(str(key), value)
        return value
