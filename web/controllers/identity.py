#!/usr/bin/env python
# coding=utf-8

from commons.baseHandler import BaseHandler
import io
from commons import check_code
from service import accountService as AS

class CheckCodeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        mstream = io.BytesIO()
        img, code = check_code.create_validate_code()
        img.save(mstream, 'GIF')
        # self.session['CheckCode'] = code
        self.write(mstream.getvalue())


class CheckUserHandler(BaseHandler):
    def post(self):
        username = self.get_argument('username', None)
        print(username)
        if username:
            ret = True if AS.isExistUser(username) else False   # 存在的话返回Ture
            print(ret)
            self.write(ret)
