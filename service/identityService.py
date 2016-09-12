#!/usr/bin/env python
# coding=utf-8

from dao.DaoFactory import *
import datetime
from web.commons import generate_str
from web.commons import sendemail

def isExistUser(username):
    userInfo = UserInfoFactory.get_dao()
    return userInfo.fetchByUsername(username)


def isExistEmail(email):
    userInfo = UserInfoFactory.get_dao()
    return userInfo.fetchByEmail(email)


def emailCode(email):
    current_date = datetime.datetime.now()
    random_code = generate_str.generate_yzm()
    sendemail.email([email, ], random_code)

    sendMsgObj = SendMsgFactory.get_dao()
    ret_dict = {}
    code_count = sendMsgObj.fetchCount(email)  # 获取该邮箱已经发送code的次数
    if not code_count:
        sendMsgObj.insertCode(email, random_code, current_date)     # 第一次插入数据验证码数据
        ret_dict['status'] = 'True'
    else:            # 判断一个小时内发送验证码的次数是不是大于限定的
        limit_day = current_date - datetime.timedelta(hours=1)
        ret = sendMsgObj.fetchCountBytime(email, limit_day)
        if ret:
            ret_dict['status'] = 'False'
            ret_dict['msg'] = '已经超过今日最大次数（1小时后重试）'
        else:
            unfreeze = sendMsgObj.fetchCountOverDate(email, limit_day)  # 超过了一个小时，将以前的次数清零
            if unfreeze:
                sendMsgObj.clearTimes(email)
            sendMsgObj.flashTimes(email, current_date, random_code)  # 跟新次数
            ret_dict['status'] = 'True'
    return ret_dict