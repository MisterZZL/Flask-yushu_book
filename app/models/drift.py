from app.libs.enum import PendingStatus
from app.models.base import base

from sqlalchemy import Column, Integer, String, SmallInteger


class Drift(base):
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(30), nullable=False)
    address = Column(String(200), nullable=False)
    message = Column(String(20))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_image = Column(String(100))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(30))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(30))

    # 状态：赠送成功/等待赠送/撤销赠送/拒绝等四种状态
    # 在libs中定义了一个枚举类
    # 默认为1，等待
    # pending = Column(SmallInteger, default=1)


    _pending = Column('pending',SmallInteger,default=1)

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self,status):
        self._pending = status.value
