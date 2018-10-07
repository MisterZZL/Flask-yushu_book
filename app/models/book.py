from sqlalchemy import Column, Integer, String, Text
from app.models.base import base


class Book(base):
    # primary_key=True,唯一主键
    # autoincrement=True，自增
    id = Column(Integer, primary_key=True, autoincrement=True)

    # nullable=False,不能为空
    title = Column(String(64), nullable=False)

    # default="未知"，没有作者时，默认为作者"未知"
    author = Column(String(32), default="未知")

    binding = Column(String(32))  # 装帧版本（平装，精装）
    publisher = Column(String(50))  # 出版社
    price = Column(String(20))  # 价格
    pages = Column(Integer)
    pubdate = Column(String(20))  # 出版日期

    # unique=True,不能重复，唯一索引
    isbn = Column(String(15), nullable=False, unique=True)

    summary = Column(Text(1000))  # 简介
    image = Column(String(50))
