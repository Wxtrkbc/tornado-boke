#!/usr/bin/env python
# coding=utf-8

import datetime
import json

from web.commons.baseHandler import BaseHandler
from service import adminService
from web.commons import login_auth, admin_pager, create_table


class LoginHandler(BaseHandler):
    def get(self):
        self.render('admin/login.html')

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        if username and password:
            admin_obj = adminService.adminLogin(username, password)
            if not admin_obj:
                self.render('admin/login.html')
            else:
                self.session['admin_is_login'] = True
                self.session['admin_user_username'] = username
            self.redirect('/manage')


class ManageHandler(BaseHandler):
    @login_auth.auth_admin_render
    def get(self):
        admin_username = self.session['admin_user_username']
        user_list = adminService.fetchUser()[0:5]
        user_count = adminService.fetchUserCount()
        page = admin_pager.Pagenation(1, user_count, 5)
        str_page = page.generate_str_page()
        self.render(
            'admin/manage.html',
            admin_username=admin_username,
            page=str_page,
            user_list=user_list
        )


class PageHandler(BaseHandler):
    def post(self):
        page = self.get_argument('page', None)
        if page:
            user_count = adminService.fetchUserCount()
            user_list = adminService.fetchUser()[(int(page) - 1) * 5:int(page) * 5]
            page = admin_pager.Pagenation(1, user_count, 5)
            str_page = page.generate_str_page()
            table_body = create_table.CreateTableBody(user_list)
            self.write({'page': str_page, 'tbody': table_body})


class UserAddHandler(BaseHandler):
    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        email = self.get_argument('email', None)
        user_type = self.get_argument('user_type', None)
        ctime = datetime.datetime.now()
        ret = adminService.insertUser(username, password, email, ctime)
        self.write(str(ret))


class UserUpdateHandler(BaseHandler):
    def post(self):
        update_data_str = self.get_argument('data', None)
        if update_data_str:
            update_data_list = json.loads(update_data_str)
            for user in update_data_list:
                update_data = user
                adminService.updateUser(**update_data)


class UserDeleteHandler(BaseHandler):
    def post(self, *args, **kwargs):
        id_list_str = self.get_argument('id_list', None)
        if id_list_str != '[]':
            id_list = json.loads(id_list_str)
            adminService.deleteUser(id_list)
