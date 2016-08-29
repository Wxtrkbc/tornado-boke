#!/usr/bin/env python
# coding=utf-8

import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dao import SqlAchemyOrm as ORM
from sqlalchemy import and_, or_
from sqlalchemy.sql import func


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
    def fetchByUE(self, user, pwd):
        return self.conn.query(ORM.UserInfo).filter(
            or_(
                and_(ORM.UserInfo.username == user, ORM.UserInfo.password == pwd),
                and_(ORM.UserInfo.email == user, ORM.UserInfo.password == pwd),
            )
        ).first()

    def insetUser(self, username, password, email, ctime):
        user = ORM.UserInfo(username=username, password=password, email=email, ctime=ctime)
        self.conn.add(user)
        self.conn.commit()

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


class ArticleCategoryDao:
    def __init__(self):
        self.db_conn = DBConnection()
        self.conn = self.db_conn.connect()

    def fetchCount(self):
        return self.conn.query(ORM.ArticleCategory.nid).count()

    # def fetchCategory(self, name):
    #     return self.conn.query(ORM.ArticleCategory.name,
    #                            ORM.ArticleCategory.nid,
    #                            ORM.Article.type_id,
    #                            ).filter(and_(ORM.ArticleCategory.nid == ORM.Article.type_id,
    #                                          ORM.ArticleCategory.name == name)).count()

    def fetchCategory(self, ):
        return self.conn.query(ORM.ArticleCategory.name,
                               func.sum(ORM.Article.type_id),
                               ).filter(ORM.ArticleCategory.nid == ORM.Article.type_id).group_by(
            ORM.Article.type_id).all()

    def close(self):
        self.db_conn.close()


class ArticleDao:
    def __init__(self):
        self.db_conn = DBConnection()
        self.conn = self.db_conn.connect()

    def fetchArticleCount(self):
        return self.conn.query(ORM.Article.nid).count()

    def fetchArticles(self):
        return self.conn.query(ORM.Article.url, ORM.Article.title, ORM.Article.ctime).order_by(ORM.Article.ctime.desc()).all()

    def fetchHotArticle(self):
        return self.conn.query(ORM.Article.url, ORM.Article.title).order_by(ORM.Article.pageviews.desc(),
                                                                            ORM.Article.ctime.desc())[0:8]

    def updatePageview(self, nid):
        self.conn.query(ORM.Article).filter(ORM.Article.nid == nid).update({'pageviews': ORM.Article.pageviews+1})
        self.commit()

    def fetchArticleById(self, nid):
        return self.conn.query(ORM.Article, ORM.ArticleCategory).filter(and_(
            ORM.Article.nid == nid,
            ORM.Article.type_id == ORM.ArticleCategory.nid
        )).first()

    def close(self):
        self.db_conn.close()


class ArticleCommentDao:
    def __init__(self):
        self.db_conn = DBConnection()
        self.conn = self.db_conn.connect()

    def getCountsByid(self, pid):
        return self.conn.query(ORM.ArticleComment.nid).filter(ORM.ArticleComment.article_id == pid).count()

    def close(self):
        self.db_conn.close()