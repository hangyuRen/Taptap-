# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/20 14:47
@Auth ： Jiang Pj
"""

from my_flask.models.spark_session import MySparkSession


class Popular(MySparkSession):
    def __init__(self):
        super().__init__()

    def android_hot_list(self):
        data = self.spark.sql("select game_type,cast(percent as int)as cnt from tap.android_hotest limit 5")
        data = data.rdd.map(lambda x: {'name': x[0], 'value': x[1]}).collect()
        return data

    def ios_hot_list(self):
        data = self.spark.sql("select game_type,cast(percent as int)as cnt from tap.ios_hotest limit 5")
        data = data.rdd.map(lambda x: {'name': x[0], 'value': x[1]}).collect()
        return data
