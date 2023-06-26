# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-24 15:07
@Auth ： hyuRen
"""

from pyspark.sql import SparkSession
class MySparkSession:
    def __init__(self):
        self.spark = SparkSession.builder. \
            appName("sparkSession"). \
            master("local[*]"). \
            config("spark.sql.shuffle.partition", "2"). \
            config("spark.sql.warehouse.dir", "hdfs://hadoop007:8020/user/hive/warehouse"). \
            config("hive.metastore.uris", "thrift://hadoop007:9083"). \
            enableHiveSupport(). \
            getOrCreate()