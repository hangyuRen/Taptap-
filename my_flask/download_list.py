# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-26 15:48
@Auth ： hyuRen
"""

from my_flask.models.download import Download

class DownloadList:
    def __init__(self):
        self.Download = Download()

    def download_list(self):
        ios_download = self.Download.ios_download_list()
        x_ios = ios_download.rdd.map(lambda x: x[0]).collect()
        y_ios = ios_download.rdd.map(lambda x: int(x[1])).collect()

        android_download = self.Download.android_download_list()
        x_android = android_download.rdd.map(lambda x: x[0]).collect()
        y_android = android_download.rdd.map(lambda x: int(x[1])).collect()

        return x_ios, y_ios, x_android, y_android