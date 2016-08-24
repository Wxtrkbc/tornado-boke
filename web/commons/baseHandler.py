#!/usr/bin/env python
# coding=utf-8


import sys
import os

sys.path.append(os.path.dirname(__file__))

import tornado.web
import session


# 用来在请求处理类中完成session的初始化工作
class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.session = session.SessionFactory.get_session_obj(self)
