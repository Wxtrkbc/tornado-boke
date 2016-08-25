#!/usr/bin/env python
# coding=utf-8

from commons.baseHandler import BaseHandler
import io
from commons import check_code
from service import identityService as IS


class CheckCodeHandler(BaseHandler):      # 生成4位验证码
    def get(self, *args, **kwargs):
        mstream = io.BytesIO()
        img, code = check_code.create_validate_code()
        img.save(mstream, 'GIF')
        self.session['CheckCode'] = code
        self.write(mstream.getvalue())


class CheckUserHandler(BaseHandler):    # 检查用户名是否存在
    def post(self):
        username = self.get_argument('username', None)
        if username:
            ret = 'True' if IS.isExistUser(username) else 'False'   # 存在的话返回 Ture
            self.write(ret)


class CheckEmailHandler(BaseHandler):    # 检查邮箱是否存在
    def post(self):
        email = self.get_argument('email', None)
        if email:
            ret = 'True' if IS.isExistEmail(email) else 'False'  # 存在的话返回 Ture
            self.write(ret)


class SendMsgHandler(BaseHandler):       # 向用户邮箱发送验证码，并判断数据库中该邮箱一小时内已经发送的次数
    def post(self):
        email = self.get_argument('email', None)
        ret_dict = IS.emailCode(email)
        if ret_dict['status'] == 'True':
            self.write(ret_dict['status'])
        else:
            self.write(ret_dict['msg'])



