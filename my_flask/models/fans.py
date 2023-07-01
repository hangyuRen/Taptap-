# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-28 11:35
@Auth ： hyuRen
"""
from my_flask.models.spark_session import MySparkSession


class Fans(MySparkSession):
    def __init__(self):
        super().__init__()

    def ios_fans(self):
        data = self.spark.sql("select name,cast(fans as int)as fans from tap.ios_popular_sub \
        order by fans desc limit 10")
        return data

    def android_fans(self):
        data = self.spark.sql("select name,cast(fans as int)as fans from tap.android_popular_sub \
        order by fans desc limit 10")
        return data
