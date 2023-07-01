# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-28 12:36
@Auth ： hyuRen
"""

from my_flask.models.fans import Fans


class FansList:
    def __init__(self):
        self.fans = Fans()

    def fans_list(self):
        ios_data = self.fans.ios_fans()
        x_ios = ios_data.rdd.map(lambda x: x[0]).collect()
        y_ios = ios_data.rdd.map(lambda x: int(x[1])).collect()

        android_data = self.fans.android_fans()
        x_android = android_data.rdd.map(lambda x: x[0]).collect()
        y_android = android_data.rdd.map(lambda x: int(x[1])).collect()

        return x_ios, y_ios, x_android, y_android