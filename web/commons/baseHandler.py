#!/usr/bin/env python
# coding=utf-8


import sys
import os

sys.path.append(os.path.dirname(__file__))

import tornado.web
import session


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.session = session.SessionFactory.get_session_obj(self)
