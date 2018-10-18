#!/usr/bin/env python 
# -*- coding:utf-8 -*-
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/yushu'

SECRET_KEY = '\xac\xa5\xe6\xbe\xb1\x88\xd3\xdd\x96=r2\xe2\x82\x15R\xad`\xc6WH\x7f\x12L'

RECENT_BOOK_COUNTS = 30

CACHE_TYPE = 'simple'

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '465'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = '619246759@qq.com'
MAIL_PASSWORD = 'aaaaaaaaaaaaaaaa'  #通过短信验证收到的授权码，不是qq密码（部署时记得修改）
