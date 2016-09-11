#!/usr/bin/env python
# coding=utf-8

import functools


# 简单的认证跳转
def auth_login_redirct(func):
    functools.wraps(func)

    def wrapper(self, *args, **kwargs):
        if self.session['is_login']:
            func(self, *args, **kwargs)
        else:
            self.redirect('/login')

    return wrapper


# 管理员认证
def auth_admin_render(func):
    functools.wraps(func)

    def wrapper(self, *args, **kwargs):
        if self.session['admin_is_login']:
            func(self, *args, **kwargs)
        else:
            self.render('admin/login.html')

    return wrapper
