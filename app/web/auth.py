from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from app.forms.auth import RegisterForm, LoginForm, ForgetForm
from app.models.base import db
from app.models.user import User
from . import web



@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            # user.nickname = form.nickname.data
            # user.email = form.email.data
            # user.password = form.password.data

            db.session.add(user)
            # db.session.commit()

        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            """如果用户存在，密码正确，写入cookie"""
            """session的有效时间设置"""
            import datetime
            duration = datetime.timedelta(seconds=300)
            login_user(user, remember=True, duration=duration)

            next = request.args.get('next')  # 获取request中的next属性
            if not next or not next.startswith('/'):  # 如果next不存在或者不是以‘/’开头，防止重定向的攻击
                next = url_for('web.index')  # 如果next属性不存在，跳转到index页面
            return redirect(next)
        else:
            flash('用户名或密码错误')

    return render_template('auth/login.html', form={'data': {}})


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = ForgetForm(request.form)
    if request.method == 'POST' and form.validate():
        account_email = form.email.data
        user = User.query.filter_by(email=account_email).first_or_404()
    return render_template('auth/forget_password_request.html',form = form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
