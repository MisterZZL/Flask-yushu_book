#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from app import cache
from app.libs.httper import HTTP
from flask import current_app


class YuShu_Book():
    isbn_url = 'https://api.douban.com/v2/book/isbn/{}'
    keyword_url = 'https://api.douban.com/v2/book/search?q={}&start={}&count={}'

    @classmethod
    @cache.memoize(3600)
    def search_by_isbn(cls, q):
        url = cls.isbn_url.format(q)
        result = HTTP.get(url)
        return result

    @classmethod
    @cache.memoize(3600)
    def search_by_keyword(cls, q, page):
        url = cls.keyword_url.format(q, cls.calculate_star(page), current_app.config['PER_PAGE'])
        result = HTTP.get(url)
        return result

    @staticmethod
    def calculate_star(page):
        result = (page - 1) * (current_app.config['PER_PAGE'])
        return result
