#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from web.controllers import home
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
], **settings)


if __name__ == "__main__":

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()