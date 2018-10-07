#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import jsonify, request, flash, render_template
from flask_login import current_user

from app.forms.book import SearchForm
from app.models.gitf import Gift
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.trade import TradeInfo
from app.web import web
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShu_Book


@web.route('/book/search')
def search():
    # q = request.args['q']
    # page = request.args['page']

    # 数据校验
    form = SearchForm(request.args)
    result = {}
    if form.validate():    
        # 如果数据合格
        q = form.q.data
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == 'isbn':
            date = YuShu_Book.search_by_isbn(q)
            result = BookViewModel.package_single(date, q)
        else:
            date = YuShu_Book.search_by_keyword(q, page)
            result = BookViewModel.package_collection(date, q)
        # result = json.dumps(result)
        # return result,200,{'content-type':'application/json'}
        # return jsonify(result)

    else:
        # return jsonify({'msg':'数据校验失败'})
        # return jsonify(form.errors)
        flash('搜索的关键字不符合要求，请重新输入')
    return render_template("search_result.html", books=result)


@web.route('/test')
def test1():
    from app.libs.none_local import n
    print(n.a)
    n.a = 2
    print('*' * 40)
    print(getattr(request, "a", None))
    setattr(request, 'a', 3)
    print('*' * 40)
    return ''


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gift = False             #未登录的状态下，默认在赠送清单中没有这本书
    has_in_wish = False             #未登录的状态下，默认在心愿清单中没有这本书

    if current_user.is_authenticated:                   # 判断用户是否登录
        if Gift.query.filter_by(uid=current_user.id,    #在用户的赠送清单中查找
                                isbn=isbn,
                                launched=False).first():
            has_in_gift = True                          #用户的赠送清单中有这本书，has_in_gift修改为True
        if Wish.query.filter_by(uid=current_user.id,
                                isbn=isbn,
                                launched=False).first():
            has_in_wish = True

    date = YuShu_Book.search_by_isbn(isbn)
    book = BookViewModel.handle_book_date(date)

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()#在赠送清单中查找是否存在
    trade_wishs = Wish.query.filter_by(isbn=isbn, launched=False).all()#在心愿清单中查找是否存在

    gifts = TradeInfo(trade_gifts)
    wishs = TradeInfo(trade_wishs)

    return render_template('book_detail.html', book=book,       #返回书本详情页面
                           wishes=wishs, gifts=gifts,
                           has_in_gifts=has_in_gift,
                           has_in_wishs=has_in_wish)
