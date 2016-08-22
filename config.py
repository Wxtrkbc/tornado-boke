#!/usr/bin/env python
# coding=utf-8

PY_MYSQL_CONN_DICT = {
    "host": '127.0.0.1',
    "port": 3306,
    "user": 'root',
    "passwd": '123',
    "db": 'myboke'
}

SQL_ALCHEMY_CONN_STR = "mysql+pymysql://root:123@127.0.0.1:3306/myboke"

SQL_ALCHEMY_MAX_OVERFLOW = 1

# Session类型：cache/redis/memcached
SESSION_TYPE = "cache"
# Session超时时间（秒）
SESSION_EXPIRES = 3600