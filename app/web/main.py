from flask import render_template
from flask_login import login_required

from . import web


#首页展示  最近上传
@web.route('/')
def index():
    from app.models.gitf import Gift
    recent_gifts = Gift.recent()                    #调用Gift.recent()方法获得最近上传的书
    # books = []
    # for gift in recent_gifts:
    #     books.append(Gift.books(gift))
    # books = [gift.books() for gift in recent_gifts]
    books = [gift.book for gift in recent_gifts]   #调用Gift.books方法，获取最近上传的书的详情
    return render_template('index.html',recent = books)


@web.route('/personal')
@login_required
def personal_center():

    return render_template('personal.html')
