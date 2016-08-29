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


def getArticlesCount():
    article = ArticleFactory.get_dao()
    return article.fetchArticleCount()

def getArticles():
    article = ArticleFactory.get_dao()
    return article.fetchArticles()

def updatePageviews(nid):
    article = ArticleFactory.get_dao()
    article.updatePageview(nid)


def getArticleById(nid):
    article = ArticleFactory.get_dao()
    return article.fetchArticleById(nid)

def getArticleCommnet(pid):
