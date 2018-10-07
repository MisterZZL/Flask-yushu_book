#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from flask import blueprints

web = blueprints.Blueprint('web',__name__)

from app.web import book,auth,drift,gift,main,test,wish