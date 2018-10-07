from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import SmallInteger, Column, Integer


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

db = SQLAlchemy()

class base(db.Model):
    __abstract__ =True          #抽象模型，不创建真实的表
    status = Column(SmallInteger, default=1)
    create_time = Column('create_time',Integer)


    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self,attrs_dict):
        for key,value in attrs_dict.items():
            if hasattr(self,key) and key not in ['id']:
                setattr(self,key,value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None