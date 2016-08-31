#!/usr/bin/env python
# coding=utf-8

import config
import redis
import functools


def cache(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        pool = redis.ConnectionPool(**config.REDIS_CONNECT_DIRT)
        r = redis.Redis(connection_pool=pool)
        ret = r.get('index')
        if ret:
            self.write(ret)
            return
        func(self, *args, **kwargs)
        r.set('index', self._response_html, ex=config.REDIS_PAGE_CAHE_EXPIRES)   # self._response_html为修改源码里
    return wrapper