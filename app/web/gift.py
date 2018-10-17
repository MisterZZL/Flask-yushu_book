from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.libs.enum import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gitf import Gift
from app.spider.yushu_book import YuShu_Book
from app.view_models.trade import MyTrade
from . import web


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id  # 获取用户ID
    trade_of_mine = Gift.get_user_gifts(uid)  # 获取用户想要的书
    isbn_list = [trade.isbn for trade in trade_of_mine]
    trade_count_dict = Gift.get_wish_counts(isbn_list)
    gift = MyTrade(trade_of_mine, trade_count_dict).trade

    return render_template('my_gifts.html', gifts=gift)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        """实现赠送、接收的事物操作"""
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            db.session.add(gift)
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(current_user)
            # db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:
        flash('这本书已经添加到赠送清单或已存在于心愿清单中，请不要重复添加')

    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(uid=current_user.id, id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash("这个礼物处于交易状态，请前往鱼漂完成交易")
    else:
        with db.auto_commit():
            current_user.beans += current_app.config['BEANS_TRADE_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))
