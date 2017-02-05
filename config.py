#!/usr/bin/env python
# coding=utf-8


SQL_ALCHEMY_CONN_STR = "mysql+pymysql://root:@127.0.0.1:3306/myboke?charset=utf8"

SQL_ALCHEMY_MAX_OVERFLOW = 5

REDIS_CONNECT_DIRT = {
    "host": '115.28.147.110',  # redis 连接地址ip
    "port": 6379,
}

MEMCACHED_CONNECT_LIST = [
    '115.28.147.110:12000',  # memcached 连接地址
]

# SESSION_TYPE = "redis"   # Session类型：cache/redis/memcached
SESSION_TYPE = "cache"  # Session类型：cache/redis/memcached

SESSION_EXPIRES = 3600  # Session超时时间（秒）

REDIS_PAGE_CAHE_EXPIRES = 10  # 页面缓存时间
