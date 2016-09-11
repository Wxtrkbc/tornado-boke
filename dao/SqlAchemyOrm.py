#!/usr/bin/env python
# coding=utf-8


# 该文件仅仅用来创建表结构

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, String, TIMESTAMP, TEXT
from sqlalchemy import ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
import config

ENGINE = create_engine(config.SQL_ALCHEMY_CONN_STR, max_overflow=config.SQL_ALCHEMY_MAX_OVERFLOW)

Base = declarative_base()


# 邮箱验证码表
class SendMsg(Base):
    __tablename__ = 'sendmsg'

    nid = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(4))
    email = Column(String(32), index=True)
    times = Column(Integer, default=0)
    ctime = Column(TIMESTAMP)


# 用户信息表
class UserInfo(Base):
    __tablename__ = 'userinfo'

    nid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))
    password = Column(String(32))
    email = Column(String(32))
    ctime = Column(TIMESTAMP)
    user_type = Column(Integer, default=0)   # 默认为普通用户 ，1为管理员

    # 自引用，多对多
    # followed = relationship('UserInfo', secondary='Follow.__table__',  backref='followers')

    __table_args__ = (
        Index('ix_user_pwd', 'username', 'password'),
        Index('ix_email_pwd', 'email', 'password'),
    )

    def __repr__(self):
        return "%s-%s-%s" % (self.nid, self.username, self.email)


# 文章类型表
class ArticleCategory(Base):
    __tablename__ = 'article_category'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    url = Column(String(32))


# 文章表
class Article(Base):
    __tablename__ = 'article'

    nid = Column(Integer, primary_key=True, autoincrement=True)
    user_info_id = Column(Integer, ForeignKey("userinfo.nid"))
    ctime = Column(TIMESTAMP)
    title = Column(String(32))
    url = Column(String(128))
    content = Column(TEXT)          # 概要
    main_content = Column(TEXT)     # 文章主要1内容
    type_id = Column(Integer, ForeignKey('article_category.nid'))
    pageviews = Column(Integer)




class ArticleComment(Base):
    __tablename__ = 'art_comment'

    nid = Column(Integer, primary_key=True, autoincrement=True)
    user_info_id = Column(Integer, ForeignKey("userinfo.nid"))
    article_id = Column(Integer, ForeignKey("article.nid"))
    reply_id = Column(Integer, ForeignKey("art_comment.nid"), nullable=True, default=None)
    up = Column(Integer)
    ctime = Column(TIMESTAMP)
    content = Column(String(150))



def init_db():
    Base.metadata.create_all(ENGINE)


def drop_db():
    Base.metadata.drop_all(ENGINE)





# drop_db()
# init_db()
