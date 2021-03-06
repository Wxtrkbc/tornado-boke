#!/usr/bin/env python
# coding=utf-8

from dao.DaoFactory import *


def login(form):
    userInfo = UserInfoFactory.get_dao()
    ret = userInfo.fetchByUE(form._value_dict['username'], form._value_dict['password'])
    return ret


def register(form, limit_day, rep, current_date):
    sendMsgObj = SendMsgFactory.get_dao()
    is_valid_code = sendMsgObj.fetchValidCode(form._value_dict['email'],
                                              form._value_dict['email_code'], limit_day)
    if not is_valid_code:
        rep.status = False
        rep.message['email_code'] = '邮箱验证码不正确或过期'
        return rep

    userInfo = UserInfoFactory.get_dao()  # 后端form注册时再来验证用户名和邮箱是否已经注册了
    has_exists_email = userInfo.fetchByEmail(form._value_dict['email'])
    if has_exists_email:
        rep.status = False
        rep.message['email'] = '邮箱已经存在'
        return rep

    has_exists_username = userInfo.fetchByUsername(form._value_dict['username'])
    if has_exists_username:
        rep.status = False
        rep.message['username'] = '用户名已经存在'
        return rep

    form._value_dict['ctime'] = current_date  # 插入一条用户数据
    form._value_dict.pop('email_code')
    form._value_dict.pop('check_password')
    last_nid = userInfo.insetUser(**form._value_dict)
    rep.status = True
    rep.message['last_nid'] = last_nid
    return rep

    # 这里可以将以前发送验证码的数据从数据库卸载
