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
