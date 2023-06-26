# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-21 14:58
@Auth ： hyuRen
"""

from flask import render_template
from my_flask.models import hotest_kind as hk


class PopList:
    def __init__(self):
        self.pop = hk.Popular()

    def android_hot_list(self):
        data = self.pop.android_hot_list()
        # [{'name': 'col1', 'value': 10}, {'name': 'col2', 'value': 20}, {'name': 'col3', 'value': 40}]
        return render_template("pie-roseType-simple.html", data=data)

    def ios_hot_list(self):
        data = self.pop.ios_hot_list()
        # [{'name': 'col1', 'value': 10}, {'name': 'col2', 'value': 20}, {'name': 'col3', 'value': 40}]
        return render_template("pie-roseType-simple.html", data=data)