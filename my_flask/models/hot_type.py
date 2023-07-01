# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-30 13:51
@Auth ： hyuRen
"""
from pyspark.sql.functions import split
from pyspark.sql.types import StructType, StringType

from my_flask.models.spark_session import MySparkSession

class HotTypePercent(MySparkSession):
    def __init__(self):
        super().__init__()

    def get_hot_type_percent(self):
        rdd = self.spark.read.format('csv').load('hdfs://hadoop007:8020/user/hadoop/tap/hotest.csv/hotest.csv').toDF("game_type",
                                                                                                           "percent")
        # 自定义列名
        schema = StructType().add("game_type", StringType()).add("percent", StringType())

        # 使用自定义列名创建DataFrame
        rdd = self.spark.createDataFrame(rdd.rdd, schema)
        split_col = split(rdd['percent'], ',')
        rdd = rdd.withColumn('数量', split_col.getItem(0))
        rdd = rdd.withColumn('占比', split_col.getItem(1))
        hot_type = rdd.select('game_type', '数量', '占比').collect()
        return hot_type