import redis
from django.conf import settings
import json

class RedisClient:
    _instance = None
    def __init__(self):
        cfg = settings.REDIS_CONFIG
        self.pool = redis.ConnectionPool(
            host=cfg["HOST"],
            port=cfg["PORT"],
            db=cfg["DB"],
            password=cfg["PASSWORD"],
            decode_responses=cfg["DECODE_RESPONSES"],
            max_connections=20
        )
        self.client = redis.Redis(connection_pool=self.pool)

    @classmethod
    async def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def add(self, key: str, value: str, expire_sec: int = None):
        if expire_sec:
            self.client.setex(key, expire_sec, value)
        else:
            self.client.set(key, value)

    async def get(self, key: str):
        return self.client.get(key)
    
    async def delete(self, key: str):
        return self.client.delete(key)

    async def exists(self, key: str):
        return self.client.exists(key)
    
    async def get_all(self):
        result = []
        keys = self.client.keys("*")
        for key in keys:
            k = key.decode()
            value = self.client.get(k)
            couple = {k: value.decode() if value else None}
            result.append(couple)
        return result
    
    async def queue_add(self, queue_key: str, value: dict):
        self.client.rpush(queue_key, json.dumps(value))
