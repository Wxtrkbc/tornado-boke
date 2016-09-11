#!/usr/bin/env python
# coding=utf-8

from web.commons.baseHandler import BaseHandler
from service import adminService as AS
from web.commons import login_auth

class LoginHandler(BaseHandler):

    def get(self):
        self.render('admin/login.html')

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        if username and password:
            admin_obj = AS.adminLogin(username, password)
            if not admin_obj:
                self.render('admin/login.html')
            else:
                self.session['admin_is_login'] = True
                self.session['admin_user_username'] = username
            self.redirect('/manage')


class ManageHandler(BaseHandler):
    @login_auth.auth_admin_render
    def get(self):
        admin_username = self.session['admin_username']
        self.render('admin/manage.html', admin_username=admin_username)

