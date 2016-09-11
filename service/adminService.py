#!/usr/bin/env python
# coding=utf-8

from dao.DaoFactory import *
import datetime


def adminLogin(username, password):
    userInfo = UserInfoFactory.get_dao()
    ret = userInfo.fetchAdmin(username, password)
    return ret