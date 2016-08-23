#!/usr/bin/env python
# coding=utf-8

from commons.baseHandler import BaseHandler
import io
from commons import check_code
from service import accountService as AS


class CheckCodeHandler(BaseHandler):      # 4位验证码
    def get(self, *args, **kwargs):
        mstream = io.BytesIO()
        img, code = check_code.create_validate_code()
        img.save(mstream, 'GIF')
        # self.session['CheckCode'] = code
        self.write(mstream.getvalue())


class CheckUserHandler(BaseHandler):    # 检查用户名是否存在
    def post(self):
        username = self.get_argument('username', None)
        if username:
            ret = 'True' if AS.isExistUser(username) else 'False'   # 存在的话返回 Ture
            self.write(ret)


class CheckEmailHandler(BaseHandler):    # 检查邮箱是否存在
    def post(self):
        email = self.get_argument('email', None)
        if email:
            ret = 'True' if AS.isExistEmail(email) else 'False'  # 存在的话返回 Ture
            self.write(ret)


class SendMsgHandler(BaseHandler):       # 向用户邮箱发送验证码
    def post(self):
        email = self.get_argument('email', None)
        print(email)
        self.write('True')


# ret = True if AS.isExistUser('jason') else False
        # print(ret)
