# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-26 15:48
@Auth ： hyuRen
"""
from flask import render_template

from my_flask.models.download import Download

class DownloadList:
    def __init__(self):
        self.Download = Download()

    def ios_download_num(self):
        x_ios, y_ios = self.Download.ios_download_list()
        return render_template('ios-down.html', x_ios=x_ios, y_ios=y_ios)

    def android_download_num(self):
        x_android, y_android = self.Download.android_download_list()
        return render_template('android-down.html', x_android=x_android, y_android=y_android)