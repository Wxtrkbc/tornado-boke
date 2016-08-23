#!/usr/bin/env python
# coding=utf-8

from dao.DaoFactory import *


def isExistUser(username):
    userInfo = UserInfoFactory.get_dao()
    return userInfo.fetchByUsername(username)


def isExistEmail(eamil):
    userInfo = UserInfoFactory.get_dao()
    return userInfo.fetchByUsername(eamil)


def login(username, password):
    userInfo = UserInfoFactory.get_dao()
    ret = userInfo.fetchByUP(username, password)
    if ret:
        pass
    else:
        pass