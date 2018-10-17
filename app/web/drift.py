from flask import flash, redirect, url_for, render_template, request, current_app
from flask_login import current_user, login_required
from sqlalchemy import or_, desc

from app.forms.book import DriftForm
from app.libs.emailer import send_email
from app.libs.enum import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gitf import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.drift import DriftCollection, DriftViewModel
from . import web


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
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
            subject='有人想要一本书', template='email/get_gift.html',
            gift=current_gift, wisher=current_user)
        flash(message='邮件已发送')
        return redirect(url_for('web.pending'))
    return render_template('drift.html', gifter=current_gift.user.summary, form=form)


@web.route('/pending')
@login_required
def pending():
    #   or_表示或的关系
    #   作为一个用户，你既可以送书也可以要书，那么在交易记录中，既可能是requester也可能是gifter
    #   所以这里用或的关系查找
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id)
    ).order_by(desc(Drift.create_time)).all()
    view = DriftCollection(drifts)
    return render_template('pending.html',drifts = view.data)

@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):          #拒绝
    with db.auto_commit():
        drift = Drift.query.filter_by(
            gifter_id = current_user.id,id = did).first_or_404()
        drift.pending = PendingStatus.Reject    #修改拒绝后的交易状态

        user = User.query.filter_by(id = drift.requester_id).first_or_404()
        user.beans += current_app.config['BEANS_TRADE_ONE_BOOK']

    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):          #撤销
    with db.auto_commit():
        drift = Drift.query.filter_by(
            requester_id = current_user.id,id = did).first_or_404()
        drift.pending = PendingStatus.Redraw        #修改撤销后的交易状态

        current_user.beans += current_app.config['BEANS_TRADE_ONE_BOOK']
    return redirect(url_for('web.pending'))

@web.route('/drift/<int:did>/mailed')       #已邮寄
@login_required
def mailed_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(
            gifter_id = current_user.id,id = did).first_or_404()
        drift.pending = PendingStatus.Success   #修改已邮寄后交易状态

        #已经寄出后，修改赠送者的赠送清单的状态
        gift = Gift.query.filter_by(id = drift.gifter_id).first_or_404()
        gift.launched = True        #数据库中改为launched = True ，表示已经赠送这本书

        # 已经寄出后，修改请求者的赠送清单的状态
        wish = Wish.query.filter_by(isbn = drift.isbn,uid = drift.requester_id).first_or_404()
        wish.launched = True        #数据库中改为launched = True ，表示已经得到这本书
        #Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,launched = False).update({'launched' : False})

        current_user.beans +=current_app.config['BEANS_TRADE_ONE_BOOK']

        return redirect(url_for('web.pending'))
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
        drift.isbn = book['isbn']

        current_user.beans -= current_app.config['BEANS_TRADE_ONE_BOOK']

        db.session.add(drift)  # 把drift提交到session中去（跟新到数据库中）
