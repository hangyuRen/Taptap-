# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/20 14:47
@Auth ： Jiang Pj
@Function: 1、最热门的游戏类型；2、热门游戏中各游戏类型占比
"""

from pyspark.sql import SparkSession
from collections import Counter
from collections import OrderedDict

from pyspark.sql.types import *

if __name__ == '__main__':
    spark = SparkSession.builder. \
        appName("sparkSession"). \
        master("local[*]"). \
        config("spark.sql.shuffle.partition", "2"). \
        config("spark.sql.warehouse.dir", "hdfs://hadoop007:8020/user/hive/warehouse"). \
        config("hive.metastore.uris", "thrift://hadoop007:9083"). \
        enableHiveSupport(). \
        getOrCreate()

    android_popular_data = spark.read.format('csv').option('header', 'true'). \
        load("file:///home/hadoop/python_project/flask_project/crawler/tap/android_popular.csv")
    ios_popular_data = spark.read.format('csv').option('header', 'true'). \
        load("file:///home/hadoop/python_project/flask_project/crawler/tap/ios_popular.csv")

    # 安卓
    android_popular_data = android_popular_data.toDF('name', 'rating', 'downLoadNum', 'fans',
                    'pos_count', 'neg_count', 'game_type',
                    'download_url', 'image_url', 'company_name')
    android_popular_data.createOrReplaceTempView("android_popular_data")

    android_game_type_list = android_popular_data.select("game_type"). \
        rdd.filter(lambda x: x[0] is not None).map(lambda x: x[0]).collect()


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
    # android_nums = len(android_game_type_list_1)

    # 含有统计数量和百分比
    # for k, v in android_result.items():
    #     p = round((v / android_nums) * 100, 2)
    #     str = f"{v},{p}%"
    #     android_result[k] = str
    # print(android_result)

    # 只含百分比
    # for k, v in android_result.items():
    #     p = round((v / android_nums) * 100, 2)
    #     str = f"{p}%"
    #     android_result[k] = str
    # print(android_result)

    # 存表
    schema = StructType([
        StructField("game_type", StringType(), nullable=False),
        StructField("percent", StringType(), nullable=False)
    ])

    df = spark.createDataFrame(zip(android_result.keys(), android_result.values()), schema=schema)
    df.show()
    df.write.mode("overwrite").saveAsTable("tap.android_hotest")
    # df.write.mode("overwrite").saveAsTable("bigdata.android_hotest")
    # df.show()


    # --------------------------------------------------------------------------------------

    # ios
    ios_popular_data = ios_popular_data.toDF('name', 'rating', 'downLoadNum', 'fans',
                    'pos_count', 'neg_count', 'game_type',
                    'download_url', 'image_url', 'company_name')
    ios_popular_data.createOrReplaceTempView("ios_popular_data")

    ios_game_type_list = ios_popular_data.select("game_type"). \
        rdd.filter(lambda x: x[0] is not None).map(lambda x: x[0]).collect()


    # 分割
    temp_list = []
    for game_ty in ios_game_type_list:
        temp_list.append(game_ty.split(','))
    ios_game_type_list_1 = [item for sublist in temp_list for item in sublist]

    # 统计出现次数
    # ios_nums = len(ios_game_type_list_1)
    ios_result = {}
    ios_ty_count = Counter(ios_game_type_list_1)
    for item, count in ios_ty_count.items():
        # print(f"{item}:{count}")
        ios_result.update({item: count})

    ios_result = OrderedDict(sorted(ios_result.items(), key=lambda x: x[1], reverse=True))

    # 含有统计数量和百分比
    # for k, v in ios_result.items():
    #     p = round((v / ios_nums) * 100, 2)
    #     str = f"{v},{p}%"
    #     ios_result[k] = str
    # print(ios_result)

    # 只含有百分比
    # for k, v in ios_result.items():
    #     p = round((v / ios_nums) * 100, 2)
    #     str = f"{p}%"
    #     ios_result[k] = str
    # print(ios_result)

    # 存表
    df_ios = spark.createDataFrame(zip(ios_result.keys(), ios_result.values()), schema=schema)
    df_ios.write.mode("overwrite").saveAsTable("tap.ios_hotest")
    df_ios.show()
