#!/usr/bin/env python
# coding=utf-8

from dao.DaoFactory import *
import datetime


def category():
    articleCategory = ArticleCategoryFactory.get_dao()
    count = articleCategory.fetchCount()
    category_info = articleCategory.fetchCategory()
    return (count, category_info)


def getHotArticles():
    article = ArticleFactory.get_dao()
    return article.fetchHotArticle()


def getArticlesCount(pid=None):
    article = ArticleFactory.get_dao()
    return article.fetchArticleCount(pid)

def getArticles(pid=None):
    article = ArticleFactory.get_dao()
    return article.fetchArticles(pid)

def getAll():
    article = ArticleFactory.get_dao()
    return article.fetchAll()

def updatePageviews(nid):
    article = ArticleFactory.get_dao()
    article.updatePageview(nid)


def getArticleById(nid):
    article = ArticleFactory.get_dao()
    return article.fetchArticleById(nid)


def getArticleCommnet(pid):     # 获取评论的数量
    obj = ArticleCommentFactory.get_dao()
    return obj.getCountsByid(pid)


def getCommnet(pid):                # 获取该文章的所有评论信息
    obj = ArticleCommentFactory.get_dao()
    return obj.getCommentsById(pid)