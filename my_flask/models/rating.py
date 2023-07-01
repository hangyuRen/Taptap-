# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-24 16:13
@Auth ： hyuRen
"""
from my_flask.models.spark_session import MySparkSession

class GameRating(MySparkSession):
    def __init__(self):
        super().__init__()

    def ios_rate(self):
        data = self.spark.sql("select count(*) as cnt, cast(rating as int)as rate from tap.ios_by_rating group by rate \
        order by rate")

        return data

    def android_rate(self):
        data = self.spark.sql("select count(*)as cnt, cast(rating as int)as rate \
        from tap.android_by_rating group by rate order by rate")

        return data