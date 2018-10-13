from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger, desc, func
from sqlalchemy.orm import relationship
from app.models.base import base, db
from app.models.wish import Wish
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
        # 差赠送清单列表
        # launched = False，False表示没有送出的书
        # group_by(Gift.isbn),按照isbn号，把不同的人送的同一本书分到一个组，目的是去重
        # order_by(desc(Gift.create_time))，order_by排序，desc()是降序排列，Gift.create_time赠送的时间
        # 按照赠送的时间降序排列
        # limit(current_app.config['RECENT_BOOK_COUNTS'])，限制页面最多展示的数量
        # distinct()，去重
        recent_gifts = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNTS']).distinct().all()
        return recent_gifts

    @property
    def books(self):
        date = YuShu_Book.search_by_isbn(self.isbn)  # isbn号找书，得到书详情数据date
        book = BookViewModel.handle_book_date(date)  # 通过单本书的方法处理date，提取需要的信息
        # 该方法会多次调用豆瓣API，应该使用缓存会比较好(Flask-cache)
        return book

    @classmethod
    def get_user_gifts(cls, uid):  # 定义方法，获取用户的赠送清单
        # 用户的赠送清单 = 通过用户的id，在用没有送出的书本清单中查找，按时间倒叙排序
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @staticmethod
    def get_wish_counts(isbn_list):
        # 通过传入的isbn号，到wish表中希望得到这本书的人的数量
        # query(func.count(Wish.id),Wish.isbn),count计算出有多少个id（人）想要这本书
        # 例如：输入['9787108006684','9787108006685','9787108006686']
        #      输出{'9787108006684': 1,'9787108006685': 2,'9787108006686': 3}
        # 查询数据可能会比较大，通过类似 mysql中in的方法取查找
        # filter  是表达式,所以这么用 ==  ，filter(Wish.launched == False)
        # group_by(Wish.isbn):isbn号分组
        counts_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == False,
                                                                              Wish.isbn.in_(isbn_list),
                                                                              Wish.status == 1).group_by(
            Wish.isbn).all()

        count_dict = {w[1]:w[0] for w in counts_list}       #字典推导式，得到{'9787108006684': 1,'9787108006685': 2,'9787108006686': 3}

        return count_dict
