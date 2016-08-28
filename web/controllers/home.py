#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from commons.baseHandler import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):

        self.render('home/index.html')


class articleHandler(BaseHandler):
    def get(self, pid):
        # print(pid)
        self.render('articles/{}.html'.format(pid))
