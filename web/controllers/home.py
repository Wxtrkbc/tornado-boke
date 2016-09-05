#!/usr/bin/env python
# -*- coding:utf-8 -*-


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from commons.baseHandler import BaseHandler
from commons import comment_tree
from commons import uimethods
from service import homeService as HS
from web.commons.pager import Pagenation
from web.commons import login_auth
from web.commons import page_cache
import json
import datetime


class IndexHandler(BaseHandler):

    # @page_cache.cache
    def get(self, page):
        # time = datetime.datetime.now()   用来测试缓存页面是否生效
        all_count = HS.getArticlesCount()
        page_obj = Pagenation(page, all_count, 7)           # 每页7项数据
        str_page = page_obj.generate_str_page('/index/')    # 分页
        content_list = HS.getAll()[page_obj.start_item:page_obj.end_item]
        # self.render('home/index.html', str_page=str_page, ret=content_list, time=time)
        self.render('home/index.html', str_page=str_page, ret=content_list)


class AboutHandler(BaseHandler):
    def get(self):
        self.render('about.html')

# 文章页
class articleHandler(BaseHandler):
    def get(self, pid):
        ret = HS.getArticleById(pid)                # 文章详细信息
        count_comments = HS.getArticleCommnet(pid)  # 文章评论数量
        comment_list = HS.getCommnet(pid)
        comment = comment_tree.build_tree(comment_list)  # 评论树
        HS.updatePageviews(pid)             # 跟新文章浏览量

        pre_article, next_article = HS.getPreNext(pid)
        self.render(
            'base/article_layout.html',
            ret=ret,
            count_comments=count_comments,
            comment=comment,
            pre_article=pre_article,
            next_article=next_article
        )


# 分类主页
class categoriesHandler(BaseHandler):
    def get(self):
        count, ret = HS.category()

        hot_articles = HS.getHotArticles()
        self.render('categories.html', count=count, category_info=ret, hot_articles=hot_articles)


# 总的目录
class contentsHandler(BaseHandler):
    def get(self, page=1):
        all_count = HS.getArticlesCount()
        content_str = '本站'
        page_obj = Pagenation(page, all_count, 7)   # 每页7项数据
        str_page = page_obj.generate_str_page('/contents/')
        content_list = HS.getArticles()[page_obj.start_item:page_obj.end_item]
        # old_page = self.get_cookie('page', 1)  # 回去用户上一次所在的页面信息   后面来完善

        self.render('contents.html', str_page=str_page, content_str=content_str, content_list=content_list, all_count=all_count)



# 分类目录
class categHandler(BaseHandler):
    def get(self, pid=1, page=1):
        all_count = HS.getArticlesCount(pid)
        page_obj = Pagenation(page, all_count, 7)  # 每页7项数据
        str_page = page_obj.generate_str_page('/categ/{}/'.format(pid))
        content_list = HS.getArticles(pid)[page_obj.start_item:page_obj.end_item]
        content_str = content_list[0][3]
        self.render('contents.html', str_page=str_page, content_str=content_str, content_list=content_list, all_count=all_count)



# class testHandler(BaseHandler):
#     def get(self):
#         self.render('text.html')
#
#     def post(self):
#         data = self.get_argument('data', None)
#         print(data)
#
#         # class ="brush: python; toolbar: false;
#         # self.write(data.replace('<pre', '<pre class="brush: python; toolbar: false;').replace('<br />', ''))
#         self.write(data)


class commentHandler(BaseHandler):
    # @login_auth.auth_login_redirct   # 测试认证功能
    # def get(self):
    #     self.write('sss')

    @login_auth.auth_login_redirct    # 没有登录的话直接跳转到登录页
    def post(self):
        article_id = self.get_argument('article_id', None)
        content = self.get_argument('content', None)
        reply_id = self.get_argument('reply_id', None)
        if reply_id == 'None':
            reply_id = None
        user_id = self.session['user_info']['nid']
        # user_id = 1
        HS.setComment(user_id, article_id, reply_id, content)  # 将评论数据插入到数据库

        comment_list = HS.getCommnet(article_id)                      # 从数据库将数据取出来到前端渲染
        comment = comment_tree.build_tree(comment_list)
        ret = uimethods.tree('_', comment)

        self.write(ret)


