#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests


class HTTP():
    def get(url, return_json=True):
        r = requests.get(url)#请求豆瓣的API网址
        if r.status_code == 200:#当isbn存在，status_code为200
            return r.json() if return_json else r.text
        return {} if return_json else ''#不存在，返回为空

        #     if return_json:
        #         result = r.json()
        #     else:
        #         result = r.text
        #     return result
        # else:
        #     if return_json:
        #         result = {}
        #     else:
        #         result = ''
        #     return result
