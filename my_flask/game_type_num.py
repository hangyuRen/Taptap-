# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-24 15:46
@Auth ： hyuRen
"""
from flask import render_template

from my_flask.models import type_num

class GameTypeNum:
    def __init__(self):
        self.typeNum = type_num.TypeNum()

    def get_type_num(self):
        x_data, y_data = self.typeNum.get_type_num()
        return render_template('bar-simple.html', x_data=x_data, y_data=y_data)