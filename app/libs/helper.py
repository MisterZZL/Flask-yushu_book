#!/usr/bin/env python 
# -*- coding:utf-8 -*-
def is_isbn_or_key(keyword):
    # 判断搜索的是isbn还是关键字key
    # isbn13 由13个0-9的数字组成
    # isbn10 由10个0-9的数字组成，可能出现‘-’
    keyword = keyword.strip()  # 去掉搜索框中输入内容的空格
    isbn_or_key = 'key'  # 默认搜索的是关键字，目的优化代码
    if len(keyword) == 13 and keyword.isdigit():
        isbn_or_key = "isbn"
    short_keyword = keyword.replace('-', '')
    if len(short_keyword) == 9 and short_keyword.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key
