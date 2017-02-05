#!/usr/bin/env python
# coding=utf-8

import sys
import os
from hashlib import sha1
import time
import json

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config


class SessionFactory:
    @staticmethod
    def get_session_obj(handler):
        obj = None
        if config.SESSION_TYPE == "cache":
            obj = CacheSession(handler)
        elif config.SESSION_TYPE == "memcached":
            obj = MemcachedSession(handler)
        elif config.SESSION_TYPE == "redis":
            obj = RedisSession(handler)
        return obj

    @staticmethod
    def create_session_id():
        return sha1(bytes('%s%s' % (os.urandom(16), time.time()), encoding='utf-8')).hexdigest()


class CacheSession:
    session_container = {}
    session_id = "__sessionId__"

    def __init__(self, handler):
        self.handler = handler
        client_random_str = handler.get_cookie(CacheSession.session_id, None)
        if client_random_str and client_random_str in CacheSession.session_container:
            self.random_str = client_random_str
        else:
            self.random_str = SessionFactory.create_session_id()
            CacheSession.session_container[self.random_str] = {}

        expires_time = time.time() + config.SESSION_EXPIRES
        handler.set_cookie(CacheSession.session_id, self.random_str, expires=expires_time)

    def __getitem__(self, key):
        return CacheSession.session_container[self.random_str].get(key, None)

    def __setitem__(self, key, value):
        CacheSession.session_container[self.random_str][key] = value

    def __delitem__(self, key):
        if key in CacheSession.session_container[self.random_str]:
            del CacheSession.session_container[self.random_str][key]


class RedisSession:
    session_id = "redis__sessionId__"
    import redis
    pool = redis.ConnectionPool(**config.REDIS_CONNECT_DIRT)
    r = redis.Redis(connection_pool=pool)

    def __init__(self, handler):
        self.handler = handler
        client_random_str = handler.get_cookie(RedisSession.session_id, None)
        if client_random_str and RedisSession.r.exists(client_random_str):
            self.random_str = client_random_str
        else:
            self.random_str = SessionFactory.create_session_id()
            RedisSession.r.hset(self.random_str, None, None)
        RedisSession.r.expire(self.random_str, config.SESSION_EXPIRES)

        expires_time = time.time() + config.SESSION_EXPIRES
        handler.set_cookie(RedisSession.session_id, self.random_str, expires=expires_time)

    def __getitem__(self, key):
        ret = RedisSession.r.hget(self.random_str, key)  # 返回的是字节
        if ret:
            ret_str = str(ret, encoding="utf-8")
            try:
                ret = json.loads(ret_str)  # 预防ret_str本身是字典，如果value是字典的话将其转换成字典
            except:
                ret = ret_str  # 不是字典的话，返回其本身
        return ret

        # result = r.hget(self.random_str, key)
        # if result:
        #     ret_str = str(result, encoding='utf-8')
        #     try:
        #         result = json.loads(ret_str)
        #     except:
        #         result = ret_str
        #     return result
        # else:
        #     return result

    def __setitem__(self, key, value):

        # 为什么要自己将字典dumps 是因为如果是字典的话，hset的话，直接存储的是字符串
        # 比如 {'k1': 444} 存成字符串的话就变成  "{'k1': 444}"
        # 然后上面的get话，就会loads不成功，
        if type(value) == dict:
            RedisSession.r.hset(self.random_str, key, json.dumps(value))
        else:
            RedisSession.r.hset(self.random_str, key, value)

    def __delitem__(self, key):
        RedisSession.r.hdel(self.random_str, key)


class MemcachedSession:
    import memcache
    conn = memcache.Client(config.MEMCACHED_CONNECT_LIST, debug=True, cache_cas=True)
    session_id = 'memcached__sessionId__'

    def __init__(self, handler):
        self.handler = handler
        client_random_str = handler.get_cookie(MemcachedSession.session_id, None)
        if client_random_str and MemcachedSession.conn.get(client_random_str):
            self.random_str = client_random_str
        else:
            self.random_str = SessionFactory.create_session_id()
            MemcachedSession.conn.set(self.random_str, json.dumps({}), config.SESSION_EXPIRES)

        MemcachedSession.conn.set(self.random_str, MemcachedSession.conn.get(self.random_str),
                                  config.SESSION_EXPIRES)
        expires_time = time.time() + config.SESSION_EXPIRES
        handler.set_cookie(MemcachedSession.session_id, self.random_str, expires=expires_time)

    def get_dict(self):  # 根据随机字符串去mencache里面去取session
        ret = MemcachedSession.conn.get(self.random_str)
        return json.loads(ret)

    def __getitem__(self, key):
        ret_dict = self.get_dict()
        return ret_dict.get(key, None)

    def __setitem__(self, key, value):
        ret_dict = self.get_dict()
        ret_dict[key] = value
        MemcachedSession.conn.set(self.random_str, json.dumps(ret_dict), config.SESSION_EXPIRES)

    def __delitem__(self, key):
        ret_dict = self.get_dict()
        del ret_dict[key]
        MemcachedSession.conn.set(self.random_str, json.dumps(ret_dict), config.SESSION_EXPIRES)
