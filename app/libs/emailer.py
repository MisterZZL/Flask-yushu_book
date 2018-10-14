from flask_mail import Message
from flask import current_app, render_template

from app import mail


def send_email(to,subject,template,**kwargs):
    msg = Message(subject=subject, sender=current_app.config['MAIL_USERNAME'], body='Test', recipients=[to])
    msg.html = render_template(template,**kwargs)
    mail.send(msg)
