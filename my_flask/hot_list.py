# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-21 14:58
@Auth ： hyuRen
"""

from my_flask.models import hot_type_percent as hk


class PopList:
    def __init__(self):
        self.pop = hk.Popular()

    def android_hot_list(self):
        data = self.pop.android_hot_list()
        data = data.rdd.map(lambda x: {'name': x[0], 'value': x[1]}).collect()
        # [{'name': 'col1', 'value': 10}, {'name': 'col2', 'value': 20}, {'name': 'col3', 'value': 40}]
        return data

    def ios_hot_list(self):
        data = self.pop.ios_hot_list()
        data = data.rdd.map(lambda x: {'name': x[0], 'value': x[1]}).collect()
        # [{'name': 'col1', 'value': 10}, {'name': 'col2', 'value': 20}, {'name': 'col3', 'value': 40}]
        return data