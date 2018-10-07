from sqlalchemy import Column, Integer, String, Boolean,Float
from werkzeug.security import generate_password_hash,check_password_hash

from app.libs.helper import is_isbn_or_key
from app.models.base import base
from flask_login import UserMixin
from app import login_manager
from app.models.gitf import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShu_Book


class User(base,UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname=Column(String(24),nullable=False)
    phone_number = Column(String(18),unique=True)
    _password = Column('password',String(128),nullable=True)
    email = Column(String(50),unique=True,nullable=False)
    confirmed = Column(Boolean,default=False)
    beans = Column(Float,default=0)
    send_counter = Column(Integer,default=0)
    receive_counter = Column(Integer,default=0)


    """用户注册时密码加密"""
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw):
        self._password = generate_password_hash(raw)

    """登录时校验密码"""
    def check_password(self,password):
        return check_password_hash(self._password,password)

    """cookie中是只保存id的，这里获取一下id，方便log_user()使用,
       方法名就用get_id(),因为是重写了flask_login（UserMixin）模块中的一个方法。
       如果User()继承了UserMixin,就不需要下面再重写了，本例中已经继承，故注释了
    """
    # def get_id(self):
    #     return self.id

    def can_save_to_list(self,isbn):
        #判断是否可以加入心愿清单或者赠送清单（不能同时加入两个清单，既然自己都想要，就不可能赠送）
        #书本既不在心愿清单也不在赠送清单才能加入到这个列表
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShu_Book.search_by_isbn(isbn)
        if not yushu_book:
            return False
        gifting = Gift.query.filter_by(
            uid = self.id,isbn = isbn,launched = False).first()#查询赠送清单
        wishing = Wish.query.filter_by(
            uid=self.id, isbn=isbn, launched=False).first()    #查询心愿清单

        if not gifting and not wishing:
            return True
        else:
            return False


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))






