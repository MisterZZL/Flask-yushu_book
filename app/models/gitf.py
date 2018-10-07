from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import base


class Gift(base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    # book = relationship('Book')
    # bid = Column(Integer,ForeignKey('book.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)


