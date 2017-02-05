#!/usr/bin/env python
# coding=utf-8

from dao import PyORM


class UserInfoFactory:
    __dao = PyORM.UserInfoDao()

    @staticmethod
    def set_dao(dao):
        UserInfoFactory.__dao = dao

    @staticmethod
    def get_dao():
        return UserInfoFactory.__dao


class SendMsgFactory:
    __dao = PyORM.SendMsgDao()

    @staticmethod
    def set_dao(dao):
        SendMsgFactory.__dao = dao

    @staticmethod
    def get_dao():
        return SendMsgFactory.__dao


class ArticleCategoryFactory:
    __dao = PyORM.ArticleCategoryDao()

    @staticmethod
    def set_dao(dao):
        ArticleCategoryFactory.__dao = dao

    @staticmethod
    def get_dao():
        return ArticleCategoryFactory.__dao


class ArticleFactory:
    __dao = PyORM.ArticleDao()

    @staticmethod
    def set_dao(dao):
        ArticleFactory.__dao = dao

    @staticmethod
    def get_dao():
        return ArticleFactory.__dao


class ArticleCommentFactory:
    __dao = PyORM.ArticleCommentDao()

    @staticmethod
    def set_dao(dao):
        ArticleCommentFactory.__dao = dao

    @staticmethod
    def get_dao():
        return ArticleCommentFactory.__dao
