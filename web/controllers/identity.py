#!/usr/bin/env python
# coding=utf-8

from commons.baseHandler import BaseHandler
import io
from commons import check_code


class CheckCodeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        mstream = io.BytesIO()
        img, code = check_code.create_validate_code()
        img.save(mstream, 'GIF')
        # self.session['CheckCode'] = code
        self.write(mstream.getvalue())