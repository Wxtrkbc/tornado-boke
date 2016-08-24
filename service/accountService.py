#!/usr/bin/env python
# coding=utf-8

from dao.DaoFactory import *
import datetime

def login(username, password):
    userInfo = UserInfoFactory.get_dao()
    ret = userInfo.fetchByUP(username, password)
    if ret:
        pass
    else:
        pass


def register(form, limit_day, rep):
    sendMsgObj = SendMsgFactory.get_dao()
    is_valid_code = sendMsgObj.fetchValidCode(form._value_dict['email'], form._value_dict['email_code'], limit_day)
    if not is_valid_code:
        rep.message['email_code'] = '邮箱验证码不正确或过期'
        return rep

