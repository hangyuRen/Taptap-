# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/21 10:21
@Auth ： Jiang Pj
@Function：  游戏关注排行榜：1、Android、iOS：粉丝量、评分、近一个月的好评量、好评率、
            2、其他各类型：根据点击量、和粉丝量进行分析
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


    options = ['acgn', 'action', 'addictive', 'adventure',
               'apocalypse', 'card', 'casual', 'chinese_style',
               'fighting', 'healing', 'idle', 'intelligence',
               'mmorpg', 'moba', 'multi_player', 'music',
               'open_world', 'otome_game', 'pixel', 'puzzle',
               'racing', 'rogue_like', 'rpg', 'sand_box',
               'shooter', 'simulation', 'single_player',
               'strategy', 'survival', 'swords_man', 'tap_exclusive',
               'tower_defence', 'word'
               ]

    # 各类别游戏
    for x in options:
        path = 'file:///home/hadoop/python_project/flask_project/crawler/tap/'
        path = path + str(x) + '.csv'
        data = spark.read.format('csv').option('header', 'true').load(path)
        data = data.toDF('name', 'rating', 'downLoadNum', 'fans', 'game_type')
        data.createOrReplaceTempView("data")

        # 首先考虑粉丝量,下载量,评分
        table_name = 'tap.' + x + '_sub'
        sorted_data = spark.sql("select name, fans, downLoadNum, rating, game_type from data \
                        order by cast(fans as int) desc , cast(downLoadNum as int) desc, cast(rating as int) desc ")
        # sorted_data.show()
        sorted_data.write.mode("overwrite").saveAsTable(table_name)


    # 热门榜
    for x in ['android_popular', 'ios_popular']:
        path = 'file:///home/hadoop/python_project/flask_project/crawler/tap/'
        path = path + x + '.csv'
        data = spark.read.format('csv').option('header', 'true').load(path)
        data = data.toDF('name', 'rating', 'downLoadNum', 'fans',
                    'pos_count', 'neg_count', 'game_type',
                    'download_url', 'image_url', 'company_name')
        data.createOrReplaceTempView("data")

        # 权重：粉丝量、评分、好评量、好评率(下载量有0的情况)
        table_name = 'tap.' + x + '_sub'
        sorted_data = spark.sql("select name, fans, rating, pos_count, \
                            round(cast(pos_count as int)/(cast(pos_count as int) + cast(neg_count as int)), 2) as pos_rate, \
                            neg_count, downLoadNum, game_type, download_url, image_url, company_name from data \
                            order by cast(fans as int) desc , cast(rating as int) desc, \
                                  cast(pos_count as int) desc, cast(pos_rate as int) desc")
        # sorted_data.show()
        sorted_data.write.mode("overwrite").saveAsTable(table_name)


    # # 测试
    # name = 'android_popular'
    # path = 'file:///home/hadoop/data/tap/'
    # path = path + name + '.csv'
    # # data = str(option) + "_type_data"
    # data = spark.read.format('csv').option('header', 'true').load(path)
    # data = data.toDF('name', 'rating', 'downLoadNum', 'fans', \
    #                 'pos_count', 'neg_count', 'game_type',\
    #                 'download_url', 'image_url', 'company_name')
    # data.createOrReplaceTempView("data")
    #
    # table_name = 'bigdata.' + name + '_sub'
    #
    # sorted_data = spark.sql("select name, fans, rating, pos_count, \
    #                 round(cast(pos_count as int)/(cast(pos_count as int) + cast(neg_count as int)), 2) as pos_rate, \
    #                 neg_count, downLoadNum, game_type, download_url, image_url, company_name from data \
    #                 order by cast(fans as int) desc , cast(rating as int) desc, \
    #                       cast(pos_count as int) desc, cast(pos_rate as int) desc")
    # sorted_data.show()
    # # sorted_data.write.mode("overwrite").saveAsTable(table_name)

