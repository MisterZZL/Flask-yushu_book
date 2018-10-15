from flask import flash, redirect, url_for, render_template, request
from flask_login import current_user

from app.forms.book import DriftForm
from app.libs.emailer import send_email
from app.models.base import db
from app.models.drift import Drift
from app.models.gitf import Gift
from . import web


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
def send_drift(gid):  # gid = 是被赠送的书本的id，也就是礼物的id
    current_gift = Gift.query.get_or_404(gid)  # 通过gid去查到集体是那一本书

    # 判断自己是不是赠送这本书的人
    if current_gift.is_yourself_gift(current_user.id):
        flash(message='这本书是你自己的，不能向你自己索要书籍')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    # 判断鱼斗是否满足条件
    # 要求每收到两本书就要送出一本书
    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        send_email(
            to=current_gift.user.email,
            subject='有人想要一本书',template='email/get_gift.html',
            gift = current_gift,wisher = current_user)
        flash(message='邮件已发送')
    return render_template('drift.html', gifter=current_gift.user, form=form)


@web.route('/pending')
def pending():
    pass


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    pass


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass


# 记录交易信息
def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        # drift.message = drift_form.message.data
        # drift.address = drift_form.address.data

        # 使用这种drift_form.populate_obj()方法时，forms目录
        # #下的book.py中的字段名称要跟models中drift.py下中的字段要相同
        drift_form.populate_obj(drift)  # 记录表单中的信息

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = current_gift.book  # 记录书本信息
        drift.book_title = book['title']
        drift.book_author = book['author']
        drift.book_image = book['image']
        c = book['isbn']
        drift.isbn = book['isbn']

        current_user.beans -= 1

        db.session.add(drift)   #把drift提交到session中去（跟新到数据库中）
