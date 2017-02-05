#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from web.controllers import home
from web.controllers import account
from web.controllers import identity
from web.controllers import admin
from web.commons import uimethods as mt
import tornado.autoreload

settings = {
    'template_path': 'web/views',
    'static_path': 'web/static',
    "cookie_secret": 'wxtrkbc',
    # 'autoreload': True,
    'debug': True,
    'ui_methods': mt,
}

application = tornado.web.Application([
    (r"/index/(?P<page>\d*)", home.IndexHandler),
    (r"/register", account.RegisterHandler),
    (r"/login", account.LoginHandler),
    (r"/logout", account.LogoutHandler),
    (r"/about", home.AboutHandler),
    (r"/check_code", identity.CheckCodeHandler),  # 随机验证码
    (r"/check_username", identity.CheckUserHandler),  # 检查用户名是否存在
    (r"/check_email", identity.CheckEmailHandler),  # 检查邮箱是否存在
    (r"/send_msg", identity.SendMsgHandler),  # 向用户注册邮箱发送验证码

    (r'/articles/(?P<pid>\d*)', home.ArticleHandler),  # 相应文章
    (r'/categories', home.CategoriesHandler),  # 分类
    (r'/contents/(?P<page>\d*)', home.ContentsHandler),  # 目录

    (r'/categ/(?P<pid>\d*)/(?P<page>\d*)', home.CategHandler),  # 分类目录
    (r'/send_comment', home.CommentHandler),  # 处理发布的评论
    (r'/admin-login', admin.LoginHandler),  # 管理员登陆
    (r'/manage', admin.ManageHandler),  # 管理员处理页面

    (r"/user_add", admin.UserAddHandler),
    (r"/user_delete", admin.UserDeleteHandler),
    (r"/update_user", admin.UserUpdateHandler),
    (r"/page$", admin.PageHandler),  # ajax 分页取数据

], **settings)

if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
    # instance = tornado.ioloop.IOLoop.instance()
    # tornado.autoreload.start(instance)
    # instance.start()
