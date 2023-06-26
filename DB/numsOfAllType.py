# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/20 18:43
@Auth ： Jiang Pj
@Function：  分析各类型游戏的游戏数量
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit


if __name__ == '__main__':
    spark = SparkSession.builder. \
        appName("sparkSession"). \
        master("local[*]"). \
        config("spark.sql.shuffle.partition", "2"). \
        config("spark.sql.warehouse.dir", "hdfs://hadoop007:8020/user/hive/warehouse"). \
        config("hive.metastore.uris", "thrift://hadoop007:9083"). \
        enableHiveSupport(). \
        getOrCreate()

    # spark = SparkSession.builder.appName("sparkSession").master("local[*]").getOrCreate()
    # sc = spark.sparkContext


    """
    分析各游戏类型的游戏数
    """

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

    # 自行在hive中创建结果表
    # 结果表
    # create table bigdata.numsOfAllType(
    #     game_type   string,
    #     nums    string
    # )row format delimited fields terminated by ',';

    # 路径
    for x in options:
        path = 'file:///home/hadoop/python_project/flask_project/crawler/tap/'
        path = path + str(x) + '.csv'
        data = spark.read.format('csv').option('header', 'true').load(path)
        data = data.toDF('name', 'rating', 'downLoadNum', 'fans', 'game_type')
        data.createOrReplaceTempView("data")

        rdd = spark.sql("select count(*) from data")
        rdd.show()
        new_df = rdd.withColumn('game_type_name', lit(x))
        new_df = new_df.select('game_type_name', *rdd.columns)
        new_df.show()

        new_df.write.mode("append").insertInto("tap.numsOfAllType")


