#!/usr/bin/env python
# coding=utf-8

from dao.DaoFactory import *


def adminLogin(username, password):
    userInfo = UserInfoFactory.get_dao()
    ret = userInfo.fetchAdmin(username, password)
    return ret


def fetchUser():
    userInfo = UserInfoFactory.get_dao()
    ret = userInfo.fetchUser()
    return ret


def fetchUserCount():
    userInfo = UserInfoFactory.get_dao()
    ret = userInfo.fetchUserCount()
    return ret


def insertUser(username, password, email, ctime):
    userInfo = UserInfoFactory.get_dao()
    ret = userInfo.insetUser(username, password, email, ctime)
    return ret


def deleteUser(id_list):
    userInfo = UserInfoFactory.get_dao()
    userInfo.deleteUserById(id_list)


def updateUser(**update_data):
    userInfo = UserInfoFactory.get_dao()
    userInfo.updateUser(**update_data)
