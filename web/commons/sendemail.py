#!/usr/bin/env python
# coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def email(email_list, content, subject="melody's blog--Register"):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(["melody's blog", 'liujianzuo88888@126.com'])
    msg['Subject'] = subject

    server = smtplib.SMTP("smtp.126.com", 25)
    server.login("liujianzuo88888@126.com", '123qweasd')
    server.sendmail('liujianzuo88888@126.com', email_list, msg.as_string())
    server.quit()
