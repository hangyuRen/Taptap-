# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/21 10:20
@Auth ： Jiang Pj
@Function:  Android、iOS游戏下载排行榜
"""

from pyspark.sql import SparkSession

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

    android_popular_data = android_popular_data.toDF('name', 'rating', 'downLoadNum', 'fans',
                    'pos_count', 'neg_count', 'game_type',
                    'download_url', 'image_url', 'company_name')
    android_popular_data.createOrReplaceTempView("android_popular_data")

    sorted_android_by_downLoad = spark.sql("select * \
            from android_popular_data order by cast(downLoadNum as int) desc ")
    sorted_android_by_downLoad.show()

    # 存表
    sorted_android_by_downLoad.write.mode("overwrite").saveAsTable("tap.android_by_downLoad")

    # ---------------------------------------------------------------------------------------------

    ios_popular_data = ios_popular_data.toDF('name', 'rating', 'downLoadNum', 'fans',
                    'pos_count', 'neg_count', 'game_type',
                    'download_url', 'image_url', 'company_name')
    ios_popular_data.createOrReplaceTempView("ios_popular_data")

    sorted_ios_by_downLoad = spark.sql("select * \
            from ios_popular_data order by cast(downLoadNum as int) desc ")
    sorted_ios_by_downLoad.show()

    # 存表
    sorted_ios_by_downLoad.write.mode("overwrite").saveAsTable("tap.ios_by_downLoad")
