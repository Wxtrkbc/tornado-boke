#!/usr/bin/env python
# coding=utf-8

from commons.baseHandler import BaseHandler


class RegisterHandler(BaseHandler):

    def get(self):

        self.render('account/register.html')

    def post(self):
        pass

class LoginHandler(BaseHandler):

    def get(self):
        self.render('account/login.html')

    def post(self):
        pass