#!/usr/bin/env python
# coding=utf-8

import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dao import SqlAchemyOrm as ORM
from sqlalchemy import and_, or_
from sqlalchemy.sql import func
from web.commons.generate_str import generate_password


# 用来连接数据库
class DBConnection:
    def __init__(self):
        self.__conn_str = config.SQL_ALCHEMY_CONN_STR
        self.__max_overflow = config.SQL_ALCHEMY_MAX_OVERFLOW
        self.conn = None

    def connect(self):
        engine = create_engine(self.__conn_str, max_overflow=self.__max_overflow)
        session = sessionmaker(bind=engine, expire_on_commit=False)
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
        ret = self.conn.query(ORM.UserInfo).filter(ORM.UserInfo.username == username).first()
        self.db_conn.close()
        return ret

    # 通过email
    def fetchByEmail(self, email):
        ret = self.conn.query(ORM.UserInfo).filter(ORM.UserInfo.email == email).first()
        self.db_conn.close()
        return ret

    # 通过用户名和密码
    def fetchByUE(self, user, pwd):
        ret = self.conn.query(ORM.UserInfo).filter(
            or_(
                and_(ORM.UserInfo.username == user, ORM.UserInfo.password == generate_password(pwd)),
                and_(ORM.UserInfo.email == user, ORM.UserInfo.password == generate_password(pwd)),
            )
        ).first()
        self.db_conn.close()
        return ret

    def deleteUserById(self, id_list):
        self.conn.query(ORM.UserInfo).filter(ORM.UserInfo.nid.in_(id_list)).delete(synchronize_session='fetch')
        self.db_conn.close()

    def insetUser(self, username, password, email, ctime):
        user = ORM.UserInfo(username=username, password=generate_password(password), email=email, ctime=ctime)
        self.conn.add(user)
        self.conn.flush()
        self.conn.refresh(user)
        last_nid = user.nid
        self.db_conn.close()
        return last_nid

    def updateUser(self, **update_data):
        nid = update_data.pop('nid')
        self.conn.query(ORM.UserInfo).filter(ORM.UserInfo.nid == nid).update(update_data)
        self.db_conn.close()

    # 获取管理员账号和密码
    def fetchAdmin(self, user, pwd):
        ret = self.conn.query(ORM.UserInfo).filter(
            and_(
                ORM.UserInfo.username == user,
                ORM.UserInfo.password == generate_password(pwd),
                ORM.UserInfo.user_type == 1,
            ),
        ).first()
        self.db_conn.close()
        return ret

    def fetchUserCount(self):
        ret = self.conn.query(ORM.UserInfo.nid).count()
        self.db_conn.close()
        return ret

    def fetchUser(self, ):
        ret = self.conn.query(ORM.UserInfo).order_by(ORM.UserInfo.ctime.desc()).all()
        self.db_conn.close()
        return ret


class SendMsgDao:
    def __init__(self):
        self.db_conn = DBConnection()
        self.conn = self.db_conn.connect()

    # 判断该email下已经发送验证码的次数
    def fetchCount(self, email):
        ret = self.conn.query(ORM.SendMsg).filter_by(email=email).count()
        self.db_conn.close()
        return ret

    def fetchCountOverDate(self, email, limit_day):
        ret = self.conn.query(ORM.SendMsg).filter(ORM.SendMsg.email == email, ORM.SendMsg.ctime < limit_day).count()
        self.db_conn.close()
        return ret

    def clearTimes(self, email):
        self.conn.query(ORM.SendMsg).filter_by(email=email).update({"times": 0})
        self.db_conn.close()

    def flashTimes(self, email, current_date, code):
        self.conn.query(ORM.SendMsg).filter_by(email=email).update({"times": ORM.SendMsg.times + 1,
                                                                    "code": code,
                                                                    "ctime": current_date},
                                                                   synchronize_session="evaluate")

        self.db_conn.close()

    def fetchCountBytime(self, email, limit_day):
        ret = self.conn.query(ORM.SendMsg).filter(ORM.SendMsg.email == email,
                                                  ORM.SendMsg.ctime > limit_day,
                                                  ORM.SendMsg.times >= 10,
                                                  ).count()
        self.db_conn.close()
        return ret

    def insertCode(self, email, code, time):
        code = ORM.SendMsg(code=code, email=email, ctime=time)
        self.conn.add(code)
        self.db_conn.close()

    def fetchValidCode(self, email, code, time):
        ret = self.conn.query(ORM.SendMsg).filter(ORM.SendMsg.email == email,
                                                  ORM.SendMsg.code == code,
                                                  ORM.SendMsg.ctime > time).count()
        self.db_conn.close()
        return ret


class ArticleCategoryDao:
    def __init__(self):
        self.db_conn = DBConnection()
        self.conn = self.db_conn.connect()

    def fetchCount(self):
        ret = self.conn.query(ORM.ArticleCategory.nid).count()
        self.db_conn.close()
        return ret

    def fetchCategory(self):
        ret = self.conn.query(ORM.ArticleCategory.name,
                              ORM.ArticleCategory.url,
                              func.count(ORM.Article.type_id),
                              ).join(ORM.Article, isouter=True).group_by(
            ORM.Article.type_id).all()
        self.db_conn.close()
        return ret


class ArticleDao:
    def __init__(self):
        self.db_conn = DBConnection()
        self.conn = self.db_conn.connect()

    def fetchArticleCount(self, pid):
        if not pid:
            ret = self.conn.query(ORM.Article.nid).count()
        else:
            ret = self.conn.query(ORM.Article.nid).filter(ORM.Article.type_id == pid).count()
        self.db_conn.close()
        return ret

    def fetchPreNext(self, pid):
        pre_article = self.conn.query(ORM.Article.url, ORM.Article.title).filter(
            ORM.Article.nid == int(pid) - 1).first()
        next_article = self.conn.query(ORM.Article.url, ORM.Article.title).filter(
            ORM.Article.nid == int(pid) + 1).first()
        self.db_conn.close()
        return pre_article, next_article

    def fetchArticles(self, pid):
        if not pid:
            ret = self.conn.query(ORM.Article.url, ORM.Article.title, ORM.Article.ctime).order_by(
                ORM.Article.ctime.desc()).all()
        else:
            ret = self.conn.query(ORM.Article.url, ORM.Article.title, ORM.Article.ctime,
                                  ORM.ArticleCategory.name).filter(and_(
                ORM.Article.type_id == pid,
                ORM.Article.type_id == ORM.ArticleCategory.nid)).order_by(ORM.Article.ctime.desc()).all()
        self.db_conn.close()
        return ret

    def fetchHotArticle(self):
        ret = self.conn.query(ORM.Article.url, ORM.Article.title).order_by(ORM.Article.pageviews.desc(),
                                                                           ORM.Article.ctime.desc())[0:8]
        self.db_conn.close()
        return ret

    def updatePageview(self, nid):
        self.conn.query(ORM.Article).filter(ORM.Article.nid == nid).update({'pageviews': ORM.Article.pageviews + 1})
        self.db_conn.close()

    def fetchArticleById(self, nid):
        ret = self.conn.query(ORM.Article, ORM.ArticleCategory).filter(and_(
            ORM.Article.nid == nid,
            ORM.Article.type_id == ORM.ArticleCategory.nid
        )).first()
        self.db_conn.close()
        return ret

    def fetchAll(self):
        ret = self.conn.query(
            ORM.Article,
            ORM.ArticleCategory.name,
            ORM.ArticleCategory.url,
        ).filter(ORM.Article.type_id == ORM.ArticleCategory.nid).order_by(ORM.Article.ctime.desc()).all()
        self.db_conn.close()
        return ret


class ArticleCommentDao:
    def __init__(self):
        self.db_conn = DBConnection()
        self.conn = self.db_conn.connect()

    def getCountsByid(self, pid):
        ret = self.conn.query(ORM.ArticleComment.nid).filter(ORM.ArticleComment.article_id == pid).count()
        self.db_conn.close()
        return ret

    def getCommentsById(self, pid):
        ret = self.conn.query(
            ORM.ArticleComment.nid,
            ORM.ArticleComment.content,
            ORM.ArticleComment.reply_id,
            ORM.UserInfo.username,
            ORM.ArticleComment.ctime,
            ORM.ArticleComment.user_info_id,
            ORM.ArticleComment.article_id,
        ).join(ORM.UserInfo).filter(ORM.ArticleComment.article_id == pid).order_by(ORM.ArticleComment.ctime.asc()).all()
        self.db_conn.close()
        return ret

    def setComment(self, user_id, article_id, reply_id, content, ctime):
        obj = ORM.ArticleComment(
            content=content,
            reply_id=reply_id,
            article_id=article_id,
            user_info_id=user_id,
            ctime=ctime,
        )
        self.conn.add(obj)
        self.db_conn.close()
