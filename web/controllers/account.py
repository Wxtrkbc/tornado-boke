#!/usr/bin/env python
# coding=utf-8

from commons.baseHandler import BaseHandler
from web.forms import accountForm
from web.commons.baseResponse import BaseResponse
import datetime
from dao.DaoFactory import *
from service import accountService as AS

class RegisterHandler(BaseHandler):

    def get(self):
        self.render('account/register.html')

    def post(self):
        rep = BaseResponse()
        form = accountForm.RegisterForm()
        if form.valid(self):
            current_date = datetime.datetime.now()
            limit_day = current_date - datetime.timedelta(minutes=1)
            ret = AS.register(form, limit_day, rep)



class LoginHandler(BaseHandler):

    def get(self):
        self.render('account/login.html')

    def post(self):
        pass