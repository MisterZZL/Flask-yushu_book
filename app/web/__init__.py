#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import blueprints, render_template

web = blueprints.Blueprint('web',__name__)

@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html')

from app.web import book,auth,drift,gift,main,test,wish

