#!/usr/bin/env python
# coding=utf-8

PY_MYSQL_CONN_DICT = {      # pymsql 连接信息
    "host": '127.0.0.1',
    "port": 3306,
    "user": 'root',
    "passwd": '123',
    "db": 'myboke'
}

SQL_ALCHEMY_CONN_STR = "mysql+pymysql://root:123@127.0.0.1:3306/myboke"

SQL_ALCHEMY_MAX_OVERFLOW = 1


REDIS_CONNECT_DIRT = {
    "host": '192.168.46.129',   # redis 连接地址ip
    "port": 6379,
}


MEMCACHED_CONNECT_LIST = [
    '192.168.46.129:12000',    # memcached 连接地址
]


SESSION_TYPE = "cache"   # Session类型：cache/redis/memcached

SESSION_EXPIRES = 3600   # Session超时时间（秒）
