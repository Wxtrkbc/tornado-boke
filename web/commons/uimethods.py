#!/usr/bin/env python
# coding=utf-8

TEMP1 = """
<li class="items" style='padding:8px 0 0 %spx;'>
    <span class="comment" id='comment_%s'>
        <div class="comment_info" >
            <a class="name" href="javascript:void(0);">%s</a>
            <span class="content">%s</span>
            <span class="comment_time ">%s</span>
            <a class="reply_btn" href="javascript:void(0);" onclick="reply(%s,%s,'%s')"  id='comment_reply_%s' >
                回复
            </a>
        </div>
    </span>

"""


def generate_comment_html(sub_comment_dic, margin_left_val):
    html = '<ul>'
    for k, v_dic in sub_comment_dic.items():
        html += TEMP1 % (margin_left_val, k[0], k[3], k[1], k[4], k[6], k[0], k[3], k[0])
        if v_dic:
            html += generate_comment_html(v_dic, margin_left_val)
        html += "</li>"
    html += "</ul>"
    return html


def tree(self, comment_dic):
    html = ''
    for k, v in comment_dic.items():
        html += TEMP1 % (0, k[0], k[3], k[1], k[4], k[6], k[0], k[3], k[0])
        html += generate_comment_html(v, 25)
        html += "</li>"

    return html
