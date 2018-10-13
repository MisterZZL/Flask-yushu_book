from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from app.models.base import db
from app.models.wish import Wish
from app.view_models.trade import MyTrade
from . import web


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    trade_of_mine = Wish.get_user_wish(uid)
    isbn_list =[trade.isbn for trade in trade_of_mine]
    trade_count_dict = Wish.get_wish_counts(isbn_list)
    wishs = MyTrade(trade_of_mine,trade_count_dict).trade


    return render_template('my_wish.html',wishes = wishs)

@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        """实现赠送、接收的事物操作"""
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)

            # db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:
        flash('这本书已经添加到赠送清单或已存在于心愿清单中，请不要重复添加')

    return redirect(url_for('web.book_detail',isbn = isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
