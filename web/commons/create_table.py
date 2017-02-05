#!/usr/bin/env python
# coding=utf-8


TMP = '''
    <tr nid="%s">
        <td><input type="checkbox" id="%s"></td>
        <td>%s</td>
        <td edit-enable="true" edit-type="input" name="username" origin="%s">%s</td>
        <td edit-enable="true" edit-type="input" name="email" origin="%s">%s</td>
        <td edit-enable="true" edit-type="input" name="user_type" origin="%s">%s</td>
        <td edit-enable="true" edit-type="input" name="ctime" origin="%s">%s</td>
    </tr>
'''


def CreateTableBody(user_list):
    html = ''
    for user in user_list:
        html += TMP % (
            user.nid, user.nid, user.nid, user.username, user.username, user.email, user.email,
            user.user_type,
            user.user_type, user.ctime, user.ctime)
    return html
