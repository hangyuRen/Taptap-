# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-24 15:40
@Auth ： hyuRen
"""
from my_flask.models.spark_session import MySparkSession

class TypeNum(MySparkSession):
    def __init__(self):
        super().__init__()

    def get_type_num(self):
        data = self.spark.sql("select game_type,cast(num as int)as cnt from tap.all_type limit 10")

        return data