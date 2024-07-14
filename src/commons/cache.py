import logging
import pickle
from abc import ABC, abstractmethod
from typing import Any

import redis


class Cache(ABC):
    @abstractmethod
    def set(self, key: str, value: Any):
        pass

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def clean_all(self):
        pass


class RedisCache(Cache):
    def __init__(self, hostname: str, ttl: int):
        self.log = logging.getLogger(__class__.__name__)
        self.redis = redis.Redis(host=hostname, port=6379)
        self.redis.ping()
        self.ttl = ttl

    def set(self, key: str, value: Any):
        self.redis.set(key, pickle.dumps(value), ex=self.ttl)

    def get(self, key: str) -> Any:
        value = self.redis.get(key)
        if value is not None:
            return pickle.loads(value)

    def clean_all(self):
        for key in self.redis.keys():
            self.redis.delete(key)
