#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


class SearchForm(Form):
    q = StringField(DataRequired(), validators=[Length(1, 64)])
    page = IntegerField(validators=[NumberRange(1)], default=1)


class DriftForm(Form):
    recipient_name = StringField(
        validators=[DataRequired(),
                    Length(min=2, max=20, message='收件人姓名长度必须是2到20个字符之间')])

    mobile = StringField(
        validators=[DataRequired(), Regexp('^[0-9]{10}$', 0, '请输入正确的手机号码')])

    message = StringField()

    address = StringField(
        validators=[DataRequired(),
                    Length(min=10, max=100, message='地址不得少于10个字符')])
