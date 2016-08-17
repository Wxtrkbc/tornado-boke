#!/usr/bin/env python
# coding=utf-8

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import config
import generate_str


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


class CacheSession:
    session_container = {}

    def __init__(self, handler):
        self.handler = handler
        self.random_str = ''

    def __getitem__(self, item):
        random_str = self.handler.get_cookie('__session__')
        if not random_str:
            return None
        if random_str not in CacheSession.session_container.keys():
            return None
        return CacheSession.session_container[random_str].get(item, None)

    def __setitem__(self, key, value):
        random_str = self.handler.get_cookie('__session__')
        if not self.random_str:
            if not random_str:
                random_str = generate_str.generate_md5('wxtrkbc')
                CacheSession.session_container[random_str] = {}
            else:
                if random_str not in CONTAINER.keys():
                    random_str = CacheSession.__generate_str()
                    CacheSession.session_container[random_str] = {}
            self.random_str = random_str
            CacheSession.session_container[self.random_str][key] = value
        self.handler.set_cookie('__session__', self.random_str)  # 为什么放在这里，cookie可能失效？放在上面失效也一样

    def __delitem__(self, key):
        random_str = self.handler.get_cookie('__session__')
        if not random_str:
            return None
        if random_str not in CacheSession.session_container.keys():
            return None
        del CacheSession.session_container[random_str][key]


class RedisSession:
    def __init__(self, handler):
        pass


class MemcachedSession:
    def __init__(self, handler):
        pass