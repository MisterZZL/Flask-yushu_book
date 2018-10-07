#!/usr/bin/env python 
# -*- coding:utf-8 -*-
class BookViewModel():
    @classmethod
    def package_single(cls, date, keyword):
        returned = {
            'total': 0,
            'books': [],
            'keyword': keyword
        }
        if date:
            returned['total'] = 1
            returned['books'].append(cls.handle_book_date(date))
        return returned

    @classmethod
    def package_collection(cls, date, keyword):
        returned = {
            'total': date['total'],
            'books': [],
            'keyword': keyword
        }
        if date:
            returned['books'] = [cls.handle_book_date(book_item) for book_item in date['books']]
        return returned

    @classmethod
    def handle_book_date(cls,date):
        book = {
            'title': date['title'],
            'publisher': date['publisher'],
            'pages': date['pages'],
            'author': '、'.join(date['author']),
            'price': date['price'],
            'summary': date['summary'],
            'image': date['image'],
            'isbn': date.get('isbn13') or date.get('isbn10')
        }
        book['intro'] = cls.info(book)
        return book

        # 金庸/三联书店/96.0
        # 金庸/96.0
    @staticmethod
    def info(book):
        intros = filter(lambda x: True if x else False,[book.get('author'), book.get('publisher'), book.get('price')])
        return ' / '.join(intros)
