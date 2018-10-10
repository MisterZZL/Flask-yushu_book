from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger, desc
from sqlalchemy.orm import relationship
from app.models.base import base
from app.spider.yushu_book import YuShu_Book
from app.view_models.book import BookViewModel


class Gift(base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    # book = relationship('Book')
    # bid = Column(Integer,ForeignKey('book.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @staticmethod
    def recent():
        #差赠送清单列表
        #launched = False，False表示没有送出的书
        #group_by(Gift.isbn),按照isbn号，把不同的人送的同一本书分到一个组，目的是去重
        #order_by(desc(Gift.create_time))，order_by排序，desc()是降序排列，Gift.create_time赠送的时间
        #按照赠送的时间降序排列
        #limit(current_app.config['RECENT_BOOK_COUNTS'])，限制页面最多展示的数量
        #distinct()，去重
        recent_gifts = Gift.query.filter_by(launched = False).group_by(
            Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNTS']).distinct().all()
        return recent_gifts

    @property
    def books(self):
        date = YuShu_Book.search_by_isbn(self.isbn)     #isbn号找书，得到书详情数据date
        book = BookViewModel.handle_book_date(date)     #通过单本书的方法处理date，提取需要的信息
        #该方法会多次调用豆瓣API，应该使用缓存会比较好(Flask-cache)
        return book


