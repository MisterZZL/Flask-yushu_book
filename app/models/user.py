from math import floor

from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer

from app.libs.enum import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import base, db
from app import login_manager
from app.models.drift import Drift
from app.models.gitf import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShu_Book


class User(base, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)

    """用户注册时密码加密"""

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    """登录时校验密码"""

    def check_password(self, password):
        return check_password_hash(self._password, password)

    """cookie中是只保存id的，这里获取一下id，方便log_user()使用,
       方法名就用get_id(),因为是重写了flask_login（UserMixin）模块中的一个方法。
       如果User()继承了UserMixin,就不需要下面再重写了，本例中已经继承，故注释了
    """

    # def get_id(self):
    #     return self.id

    def can_save_to_list(self, isbn):
        # 判断是否可以加入心愿清单或者赠送清单（不能同时加入两个清单，既然自己都想要，就不可能赠送）
        # 书本既不在心愿清单也不在赠送清单才能加入到这个列表
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShu_Book.search_by_isbn(isbn)
        if not yushu_book:
            return False
        gifting = Gift.query.filter_by(
            uid=self.id, isbn=isbn, launched=False).first()  # 查询赠送清单
        wishing = Wish.query.filter_by(
            uid=self.id, isbn=isbn, launched=False).first()  # 查询心愿清单

        if not gifting and not wishing:
            return True
        else:
            return False

    @property
    def generater_token(self, expiration=6000):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])  # 将url中获取的token值进行反序列化
        try:
            date = s.loads(token.encode('utf-8'))
        except:
            return False

        uid = date.get('id')  # 反序列化的结果中提取到用户id
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password  # 数据库中修改用户密码，利用之前的上下文管理自动提交
        return True

    def can_send_drift(self):
        if self.beans < 1:
            return False

        success_gift_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_received_count = Drift.query.filter_by(
            requester_id=self.id,pending=PendingStatus.Success).count()
        if floor(success_received_count / 2) <= floor(success_gift_count):
            return True
        else:
            return False

    @property
    def summary(self):
        return dict(
            nickname = self.nickname,
            beans = self.beans,
            email = self.email,
            send_receive = str(self.send_counter)+'/'+str(self.receive_counter)
        )
    @property
    def send_recevie(self):
        return str(self.send_counter)+'/'+str(self.receive_counter)


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
