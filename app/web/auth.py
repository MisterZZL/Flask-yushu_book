from flask import render_template, request, redirect, url_for, flash, current_appfrom flask_login import login_user, logout_user, login_required, current_userfrom app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm, ChangePasswordFormfrom app.libs.emailer import send_emailfrom app.models.base import dbfrom app.models.user import Userfrom . import web@web.route('/register', methods=['GET', 'POST'])def register():    form = RegisterForm(request.form)    if request.method == 'POST' and form.validate():        with db.auto_commit():            user = User()            user.set_attrs(form.data)            # user.nickname = form.nickname.data            # user.email = form.email.data            # user.password = form.password.data            db.session.add(user)            # db.session.commit()        return redirect(url_for('web.login'))    return render_template('auth/register.html', form=form)@web.route('/login', methods=['GET', 'POST'])def login():    form = LoginForm(request.form)    if request.method == 'POST' and form.validate():        user = User.query.filter_by(email=form.email.data).first()        if user and user.check_password(form.password.data):            """如果用户存在，密码正确，写入cookie"""            """session的有效时间设置"""            import datetime            duration = datetime.timedelta(seconds=300)            login_user(user, remember=True, duration=duration)            next = request.args.get('next')  # 获取request中的next属性            if not next or not next.startswith('/'):  # 如果next不存在或者不是以‘/’开头，防止重定向的攻击                next = url_for('web.index')  # 如果next属性不存在，跳转到index页面            return redirect(next)        else:            flash('用户名或密码错误')    return render_template('auth/login.html', form={'data': {}})@web.route('/reset/password', methods=['GET', 'POST'])def forget_password_request():    form = EmailForm(request.form)          #请求表单提交到EmailForm中，校验是否合法    if request.method == 'POST' and form.validate():        account_email = form.email.data     #获取email账号 123456@qq.com        user = User.query.filter_by(email=account_email).first_or_404() #用户列表中查找是否存在用户        send_email(to=account_email, subject='重置密码', template='email/reset_password.html',                   token=user.generater_token, user=user)   #发送邮件        flash(message='邮件已发送')    return render_template('auth/forget_password_request.html', form=form)@web.route('/reset/password/<token>', methods=['GET', 'POST'])def forget_password(token):     #url中获取token    form = ResetPasswordForm(request.form)          #校验密码是否合法    if request.method == 'POST' and form.validate():        success = User.reset_password(token,form.password1.data) #获取新密码        if success:            flash(message='密码重置成功，请使用新的密码登录')            return redirect(url_for('web.login'))        else:            flash(message='密码重置失败')    return render_template('auth/forget_password.html')@web.route('/change/password', methods=['GET', 'POST'])def change_password():    form = ChangePasswordForm(request.form)  # 校验密码是否合法    if request.method == 'POST' and form.validate():        if current_user.check_password(form.old_password.data):            with db.auto_commit():                current_user.password = form.new_password1.data            flash('密码修改成功')            return redirect(url_for('web.login'))        else:            flash('旧密码错误')    return render_template('auth/change_password.html',form = form)@web.route('/logout')def logout():    logout_user()    return redirect(url_for('web.index'))