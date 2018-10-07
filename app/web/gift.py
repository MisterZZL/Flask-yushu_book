from flask import current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.base import db
from app.models.gitf import Gift
from . import web


@web.route('/my/gifts')
@login_required
def my_gifts():
    pass


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
def redraw_from_gifts(gid):
    pass
