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
        data = self.spark.sql("select game_type,cast(nums as int)as cnt from tap.numsOfAllType \
        where cast(nums as int) != 500")
        x_data = data.rdd.map(lambda x: x[0]).collect()
        y_data = data.rdd.map(lambda x: x[1]).collect()
        x_data.append('其他')
        y_data.append(500)
        return x_data, y_data