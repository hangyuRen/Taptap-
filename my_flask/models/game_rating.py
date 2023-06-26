# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-24 16:13
@Auth ： hyuRen
"""

from my_flask.models.spark_session import MySparkSession

class GameRating(MySparkSession):
    def __init__(self):
        super().__init__()

    def rating_top10(self):
        ios_rating = self.spark.sql("select name,cast(rating as float) from tap.ios_by_rating")
        android_rating = self.spark.sql("select name,cast(rating as float) from tap.android_by_rating")

        x_ios = ios_rating.rdd.map(lambda x: x[0]).collect()
        y_ios = ios_rating.rdd.map(lambda x: x[1]).collect()

        x_android = android_rating.rdd.map(lambda x: x[0]).collect()
        y_android = android_rating.rdd.map(lambda x: x[1]).collect()

        return x_ios, y_ios, x_android, y_android