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
            # 插入数据的时候记得直接获取一下last_nid,避免再次去数据库查询一次用户的id
            rep = AS.register(form, limit_day, rep, current_date)
            if rep.status:      # 注册成功就认为登陆了
                self.session['is_login'] = True
                form._value_dict.update({'nid': rep.message['last_nid']})
                form._value_dict.pop('ctime')
                self.session['user_info'] = form._value_dict
        else:
            rep.message = form._error_dict
        self.write(json.dumps(rep.__dict__))


class LoginHandler(BaseHandler):

    def get(self):
        self.render('account/login.html')

    def post(self):
        rep = BaseResponse()
        form = accountForm.LoginForm()
        if form.valid(self):
            if form._value_dict['check_code'].lower() != self.session["CheckCode"].lower():
                rep.message = {'check_code': '验证码错误'}
                self.write(json.dumps(rep.__dict__))
                return
            user_obj = AS.login(form)
            if not user_obj:
                rep.message = {'username': '用户名邮箱或密码错误'}
                self.write(json.dumps(rep.__dict__))
                return

            user_info_dict = {
                'nid': user_obj.nid,
                'username': user_obj.username,
                'email': user_obj.email
            }
            self.session['is_login'] = True
            self.session['user_info'] = user_info_dict
            rep.status = True

        else:
            rep.message = form._error_dict
        self.write(json.dumps(rep.__dict__))


class LogoutHandler(BaseHandler):
    def get(self):
        self.session['is_login'] = None
        self.session['user_info'] = None
        self.redirect('/index/')