from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.libs.emailer import send_email
from app.models.base import db
from app.models.drift import Drift
from app.models.gitf import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrade
from . import web


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    trade_of_mine = Wish.get_user_wish(uid)
    isbn_list = [trade.isbn for trade in trade_of_mine]
    trade_count_dict = Wish.get_wish_counts(isbn_list)
    wishs = MyTrade(trade_of_mine, trade_count_dict).trade

    return render_template('my_wish.html', wishes=wishs)


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

    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(isbn=wish.isbn, uid=current_user.id).first()

    if not gift:
        flash('你还没有上传此书，请点击“加入到赠送清单”，上传此书。添加前，请确保自己可以赠送这本书')
    else:
        send_email(to=wish.user.email,
                   subject='有人想送你一本书',
                   template='email/satisify_wish.html',
                   wish=wish, gift=gift)
        flash('已向他/她发送了一封邮件，如果他/她愿意接受你的赠送，你将受到一个鱼漂')

    return redirect(url_for('web.book_detail',isbn = wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, uid=current_user.id, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))
