# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-26 15:36
@Auth ： hyuRen
"""

from my_flask.models.spark_session import MySparkSession

class Download(MySparkSession):
    def __init__(self):
        super().__init__()

    def ios_download_list(self):
        ios_download = self.spark.sql("select name, downloadnum from tap.ios_by_downLoad limit 10")
        return ios_download

    def android_download_list(self):
        android_download = self.spark.sql("select name, downloadnum from tap.android_by_downLoad limit 10")
        return android_download