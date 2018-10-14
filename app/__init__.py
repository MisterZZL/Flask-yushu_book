#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import Flask
from flask_cache import Cache
from flask_login import LoginManager
from flask_mail import Mail

from app.models.base import db


login_manager = LoginManager()      #实例化登录模块的对象
cache = Cache()                     #实例化缓存对象

mail = Mail()


def creat_app():
    app = Flask(__name__)
    app.config.from_object('app.source')  # 引入config.py配置文件
    app.config.from_object('app.setting')
    # 调用下面的 def registe_blueprint(app)函数注册app
    # 实际上执行这句代码   web = blueprints.Blueprint('web',__name__)
    #得到一个蓝图对象
    registe_blueprint(app)

    login_manager.init_app(app)             #注册login_manager
    login_manager.login_view='web.login'    #不会报没有权限的错误，而是直接跳转到登录页面
    login_manager.login_message='请先登录或注册'  #跳转登录页面后的提示信息

    with app.app_context():             #这三行跟下面注释的两行效果一样
        db.init_app(app)
        db.create_all()
    # db.init_app(app)
    # db.create_all(app=app)

    cache.init_app(app)
    mail.init_app(app)
    return app
def registe_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
