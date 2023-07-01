# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-24 15:46
@Auth ： hyuRen
"""
from flask import render_template

from my_flask.models import type

class GameTypeNum:
    def __init__(self):
        self.typeNum = type.TypeNum()

    def get_type_num(self):
        data = self.typeNum.get_type_num()
        x_data = data.rdd.map(lambda x: x[0]).collect()
        y_data = data.rdd.map(lambda x: x[1]).collect()

        return x_data, y_data