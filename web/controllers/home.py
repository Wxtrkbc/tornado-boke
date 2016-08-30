#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from commons.baseHandler import BaseHandler
from commons import comment_tree
from service import homeService as HS
from web.commons.pager import Pagenation

class IndexHandler(BaseHandler):

    def get(self, page):
        all_count = HS.getArticlesCount()
        page_obj = Pagenation(page, all_count, 7)  # 每页7项数据
        str_page = page_obj.generate_str_page('/index/')
        content_list = HS.getAll()[page_obj.start_item:page_obj.end_item]
        self.render('home/index.html', str_page=str_page, ret=content_list)


class AboutHandler(BaseHandler):
    def get(self):
        self.render('about.html')


class articleHandler(BaseHandler):
    def get(self, pid):
        ret = HS.getArticleById(pid)
        count_comments = HS.getArticleCommnet(pid)  # 文章评论数量
        comment_list = HS.getCommnet(pid)
        comment = comment_tree.build_tree(comment_list)
        self.render('articles/{}.html'.format(pid), ret=ret, count_comments=count_comments,comment=comment)



class categoriesHandler(BaseHandler):
    def get(self):
        count, ret = HS.category()
        # for item in ret:
        #     print(item[0], item[1])
        # print(count, ret, 111)
        hot_articles = HS.getHotArticles()

        # print(hot_articles)
        self.render('categories.html', count=count, category_info=ret, hot_articles=hot_articles)


class contentsHandler(BaseHandler):
    def get(self, page=1):
        all_count = HS.getArticlesCount()
        content_str = '本站'
        page_obj = Pagenation(page, all_count, 7)   # 每页7项数据
        str_page = page_obj.generate_str_page('/contents/')
        content_list = HS.getArticles()[page_obj.start_item:page_obj.end_item]
        # old_page = self.get_cookie('page', 1)  # 回去用户上一次所在的页面信息   后面来完善

        self.render('contents.html', str_page=str_page, content_str=content_str, content_list=content_list, all_count=all_count)


class categHandler(BaseHandler):
    def get(self, pid=1, page=1):
        all_count = HS.getArticlesCount(pid)
        page_obj = Pagenation(page, all_count, 7)  # 每页7项数据
        str_page = page_obj.generate_str_page('/categ/{}/'.format(pid))
        content_list = HS.getArticles(pid)[page_obj.start_item:page_obj.end_item]
        content_str = content_list[0][3]
        self.render('contents.html', str_page=str_page, content_str=content_str, content_list=content_list, all_count=all_count)



class testHandler(BaseHandler):
    def get(self):
        self.render('text.html')