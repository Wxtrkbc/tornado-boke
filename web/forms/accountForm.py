#!/usr/bin/env python
# -*- coding:utf-8 -*-

from web.forms import forms
from web.forms import fileds


class SendMsgForm(forms.BaseForm):
    def __init__(self):
        self.email = fileds.EmailField()

        super(SendMsgForm, self).__init__()


class RegisterForm(forms.BaseForm):
    def __init__(self):
        self.username = fileds.StringField()
        self.email = fileds.EmailField()
        self.email_code = fileds.StringField()
        self.password = fileds.StringField()
        self.check_password = fileds.StringField()

        super(RegisterForm, self).__init__()


class LoginForm(forms.BaseForm):
    def __init__(self):
        self.username = fileds.StringField()
        self.password = fileds.StringField()
        self.check_code = fileds.StringField()

        super(LoginForm, self).__init__()
