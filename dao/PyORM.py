#!/usr/bin/env python
# coding=utf-8

import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dao import SqlAchemyOrm as ORM


# 用来连接数据库
class DBConnection:
    def __init__(self):
        self.__conn_str = config.SQL_ALCHEMY_CONN_STR
        self.__max_overflow = config.SQL_ALCHEMY_MAX_OVERFLOW
        self.conn = None

    def connect(self):
        engine = create_engine(self.__conn_str, max_overflow=self.__max_overflow)
        session = sessionmaker(bind=engine)
        self.conn = session()
        return self.conn

    def close(self):
        self.conn.commit()
        self.conn.close()


# 用来操作用户表的类
class UserInfoDao:
    def __init__(self):
        self.db_conn = DBConnection()
        self.conn = self.db_conn.connect()

    # 通过id
    def fetchByUsername(self, username):
        print(username, 111)
        print(self.conn.query(ORM.UserInfo).all())
        return self.conn.query(ORM.UserInfo).filter(ORM.UserInfo.username == username).first()

    # 通过用户名和密码
    def fetchByUP(self, user, pwd):
        return self.conn.query(ORM.UserInfo).filter(ORM.UserInfo.username == user, ORM.UserInfo.password == pwd).first()

    def close(self):
        self.db_conn.close()