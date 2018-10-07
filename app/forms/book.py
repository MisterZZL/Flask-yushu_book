#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from wtforms import form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


class SearchForm(form.Form):
    q = StringField(DataRequired(), validators=[Length(1, 64)])
    page = IntegerField(validators=[NumberRange(1)], default=1)
