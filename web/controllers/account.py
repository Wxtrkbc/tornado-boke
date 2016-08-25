#!/usr/bin/env python
# coding=utf-8

from commons.baseHandler import BaseHandler
from web.forms import accountForm
from web.commons.baseResponse import BaseResponse
import datetime
from dao.DaoFactory import *
from service import accountService as AS
import json


class RegisterHandler(BaseHandler):

    def get(self):
        self.render('account/register.html')

    def post(self):
        rep = BaseResponse()
        form = accountForm.RegisterForm()
        if form.valid(self):
            current_date = datetime.datetime.now()
            limit_day = current_date - datetime.timedelta(minutes=1)
            rep = AS.register(form, limit_day, rep, current_date)
            if rep.status:      # 注册成功就认为登陆了
                self.session['is_login'] = True
                self.session['user_info'] = form._value_dict
        else:
            rep.message = form._error_dict
        self.write(json.dumps(rep.__dict__))




class LoginHandler(BaseHandler):

    def get(self):
        self.render('account/login.html')

    def post(self):
        pass