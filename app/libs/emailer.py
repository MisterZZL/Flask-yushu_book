from threading import Thread

from flask_mail import Message
from flask import current_app, render_template
from app import mail

def send_async_email(app,msg):
    with app.app_context():         #推入到app_context的栈顶
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    msg = Message(subject=subject, sender=current_app.config['MAIL_USERNAME'], body='Test', recipients=[to])
    msg.html = render_template(template,**kwargs)
    # mail.send(msg)


    app = current_app._get_current_object()     #获取获取当前线程中app对象（app是被线程隔离了的）
    thr = Thread(target=send_async_email,args=(app,msg))   #开启多线程，并把app当做第一个参数传入到线程中
    thr.start()