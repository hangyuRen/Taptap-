# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/13 10:29
@Auth ： DeathboyAndBlackmaid
"""
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, trim

# 得到所有游戏数据
def getGameData(spark):
    rdd = spark.read.format('csv').option('header', 'true').load('hdfs://hadoop007:8020/user/hadoop/tap/all_kind.csv')

    # 数据去重
    rdd = rdd.drop_duplicates(['game_name'])
    data_count = rdd.count()
    # print("去重后数据量：", data_count)
    return rdd

# 用户向量和物品向量相似度计算函数
# 余弦相似度
def cosine_similarity(user_vector, item_vector):
        user_norm = np.linalg.norm(list(user_vector.values()))
        item_norm = np.linalg.norm(list(item_vector.values()))
        dot_product = np.dot(list(user_vector.values()), list(item_vector.values()))
        similarity = dot_product / (user_norm * item_norm)
        return similarity

def game_recommend(game_names):

    spark = SparkSession.builder.appName("sparkSession").master("local[*]").getOrCreate()

    data = getGameData(spark)

    # game_names = input("请输入game_name（以前玩过的且比较喜欢的游戏）（以逗号分隔）: ").split(',')

    # 根据game_name筛选相关内容
    matched_data = data.filter(data['game_name'].isin(game_names))

    # 如果没有匹配到的游戏，返回-1
    if matched_data.count() == 0:
        return -1

    # 显示匹配结果
    user_data = matched_data.dropDuplicates(['game_name'])

    # user_data.show()

    # 创建用户标签偏好向量
    # 将type区分开来
    split_types = user_data.withColumn('type', explode(split(trim(col('type')), ',')))

    # 统计向量
    type_counts = split_types.groupBy('type').count().withColumnRenamed('count', '类型数量').orderBy(
        col('类型数量').desc())

    # type_counts.show()

    # 将用户偏好向量DataFrame转换为字典
    user_preference = dict(type_counts.collect())
    # print("用户偏好量列表", user_preference)

    # 数据清洗，洗掉一些空名，空类型的，没有推荐意义的数据
    split_types = data.withColumn('type', split(col('type'), ','))
    split_types = split_types.filter(col('game_name').isNotNull() & col('type').isNotNull())
    split_types = split_types.filter(~split_types['game_name'].isin(game_names))
    # print(split_types.count())

    # 遍历所有数据，并创建物品向量列表
    item_vectors = []

    for row in split_types.collect():
        game_name = row['game_name']
        types = row['type']
        item_vector = {}

        # 根据用户偏好向量进行匹配
        for key in user_preference.keys():
            if key in types:
                item_vector[key] = 1
            else:
                item_vector[key] = 0

        item_dict = {'game_name': game_name, '物品向量': item_vector}
        item_vectors.append(item_dict)

    # 打印物品向量列表
    count = 0
    for item in item_vectors:
        if count < 5:
            # print(item['game_name'], item['物品向量'])
            count += 1
        else:
            break

    # 用户向量和物品向量相似度计算
    similarities = {}

    for item in item_vectors:
        item_name = item['game_name']
        item_vector = item['物品向量']
        similarity = cosine_similarity(user_preference, item_vector)
        similarities[item_name] = similarity

    # 过滤NaN值，也就是物品向量是零向量的情况下得到的不确定值，这是不需要的
    filtered_similarities = {game: similarity for game, similarity in similarities.items() if not np.isnan(similarity)}

    # 从大到小排序
    sorted_similarities = sorted(filtered_similarities.items(), key=lambda x: x[1], reverse=True)

    # 打印相似度结果
    count = 0
    for game, similarity in sorted_similarities:
        if count < 5:
            # print(game, similarity)
            count += 1
        else:
            break

    # 根据相似度排序的游戏列表
    sorted_game_names = [game for game, _ in sorted_similarities]

    # 创建包含排序顺序的DataFrame
    order_df = spark.createDataFrame([(game_name,) for game_name in sorted_game_names], ["game_name"])
    # 将split_types和order_df进行内连接，并按照order_df中的顺序排序
    sorted_game_data = order_df.join(split_types, on="game_name")
    # sorted_game_data.show()
    return sorted_game_data