#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from web.controllers import home
from web.controllers import account
from web.controllers import identity
import tornado.autoreload
settings = {
    'template_path': 'web/views',
    'static_path': 'web/static',
    # 'static_url_prefix': '/web/static/',
    "cookie_secret": 'wxtrkbc',
    'autoreload': True,
    'debug': True,
}

application = tornado.web.Application([
    (r"/index", home.IndexHandler),
    (r"/register", account.RegisterHandler),
    (r"/login", account.LoginHandler),
    (r"/check_code", identity.CheckCodeHandler),      # 随机验证码
    (r"/check_username", identity.CheckUserHandler),  # 检查用户名是否存在
    (r"/check_email", identity.CheckEmailHandler),    # 检查邮箱是否存在
    (r"/send_msg", identity.SendMsgHandler),          # 向用户注册邮箱发送验证码

    (r'/articles/(?P<pid>\d*)', home.articleHandler),   # 相应文章
    (r'/categories', home.categoriesHandler),              # 分类
    (r'/contents/(?P<page>\d*)', home.contentsHandler),    # 目录
], **settings)


if __name__ == "__main__":

    application.listen(8888)
    # tornado.ioloop.IOLoop.instance().start()
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()