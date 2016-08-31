#!/usr/bin/env python
# coding=utf-8
import time
import hashlib
import random

# 生成4位验证码
def generate_yzm():
    code = ''
    for i in range(4):
        current = random.randrange(0, 4)
        if current != i:
            temp = chr(random.randint(65, 90))
        else:
            temp = random.randint(0, 9)
        code += str(temp)
    return code


# 生成加密字符串
def generate_md5(value):
    r = str(time.time())
    obj = hashlib.md5(r.encode('utf-8'))
    obj.update(value.encode('utf-8'))
    return obj.hexdigest()


def generate_password(value):
    obj = hashlib.md5()
    obj.update(value.encode('utf-8'))
    return obj.hexdigest()

