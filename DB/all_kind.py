# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-29 14:32
@Auth ： hyuRen
"""

from pyspark.sql import SparkSession
from collections import Counter
from collections import OrderedDict

if __name__ == '__main__':
    spark = SparkSession.builder. \
        appName("sparkSession"). \
        master("local[*]"). \
        config("spark.sql.shuffle.partition", "2"). \
        config("spark.sql.warehouse.dir", "hdfs://hadoop007:8020/user/hive/warehouse"). \
        config("hive.metastore.uris", "thrift://hadoop007:9083"). \
        enableHiveSupport(). \
        getOrCreate()

    # 所有数据
    data = spark.read.format('csv').option('header', 'true'). \
        load("hdfs://hadoop007:8020/user/hadoop/tap/*.csv")
    data = data.drop_duplicates(['游戏名称'])
    data = data.toDF('name', 'rating', 'downLoadNum', 'fans', 'game_type')
    data.createOrReplaceTempView("data")

    android_game_type_list = data.select("game_type"). \
        rdd.filter(lambda x: x[0] is not None).map(lambda x: x[0]).collect()
    android_nums = len(android_game_type_list)
    # 分割
    temp_list = []
    for game_ty in android_game_type_list:
        temp_list.append(game_ty.split(','))
    android_game_type_list_1 = [item for sublist in temp_list for item in sublist]

    # 统计出现次数
    android_result = {}
    android_ty_count = Counter(android_game_type_list_1)
    for item, count in android_ty_count.items():
        # print(f"{item}:{count}")
        android_result.update({item: count})

    android_result = OrderedDict(sorted(android_result.items(), key=lambda x: x[1], reverse=True))
    android_nums = len(android_game_type_list_1)

    # 含有统计数量和百分比
    # for k, v in android_result.items():
    #     p = round((v / android_nums) * 100, 2)
    #     str = f"{v},{p}%"
    #     android_result[k] = str
    # print(android_result)

    # 存表
    df = spark.createDataFrame(zip(android_result.keys(), android_result.values()), schema=["game_type", "num"])
    df.show()
    df.write.mode("overwrite").saveAsTable('tap.all_type')
