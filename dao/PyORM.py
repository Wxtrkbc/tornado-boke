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

    # 通过username
    def fetchByUsername(self, username):
        return self.conn.query(ORM.UserInfo).filter(ORM.UserInfo.username == username).first()

    # 通过email
    def fetchByEmail(self, email):
        return self.conn.query(ORM.UserInfo).filter(ORM.UserInfo.email == email).first()

    # 通过用户名和密码
    def fetchByUP(self, user, pwd):
        return self.conn.query(ORM.UserInfo).filter(ORM.UserInfo.username == user, ORM.UserInfo.password == pwd).first()

    def close(self):
        self.db_conn.close()


class SendMsgDao:
    def __init__(self):
        self.db_conn = DBConnection()
        self.conn = self.db_conn.connect()

    # 判断该email下已经发送验证码的次数
    def fetchCount(self, email):
        return self.conn.query(ORM.SendMsg).filter_by(email=email).count()

    def fetchCountOverDate(self, email, limit_day):
        return self.conn.query(ORM.SendMsg).filter(ORM.SendMsg.email == email, ORM.SendMsg.ctime < limit_day).count()

    def clearTimes(self, email):
        self.conn.query(ORM.SendMsg).filter_by(email=email).update({"times": 0})
        self.conn.commit()

    def flashTimes(self, email, current_date, code):
        self.conn.query(ORM.SendMsg).filter_by(email=email).update({"times": ORM.SendMsg.times + 1,
                                                                    "code": code,
                                                                    "ctime": current_date},
                                                                   synchronize_session="evaluate")

        self.conn.commit()

    def fetchCountBytime(self, email, limit_day):
        return self.conn.query(ORM.SendMsg).filter(ORM.SendMsg.email == email,
                                                   ORM.SendMsg.ctime > limit_day,
                                                   ORM.SendMsg.times >= 10,
                                                   ).count()

    def insertCode(self, email, code, time):
        code = ORM.SendMsg(code=code, email=email, ctime=time)
        self.conn.add(code)
        self.conn.commit()

    def fetchValidCode(self, email, code, time):
        return self.conn.query(ORM.SendMsg).filter(ORM.SendMsg.email == email,
                                                   ORM.SendMsg.code == code,
                                                   ORM.SendMsg.ctime > time).count()

    def close(self):
        self.db_conn.close()
