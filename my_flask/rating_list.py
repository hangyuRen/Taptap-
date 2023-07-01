# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-24 16:28
@Auth ： hyuRen
"""

from my_flask.models import rating
class Rating:
    def __init__(self):
        self.GameRating = rating.GameRating()

    def rating(self):
        x = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10']
        x_ios, y_ios = self.ios_rate()
        x_android, y_android = self.android_rate()
        ios_data = []
        android_data = []
        for i in x:
            if i in x_ios:
                ios_data.append(y_ios[x_ios.index(i)])
            else:
                ios_data.append(0)

            if i in x_android:
                android_data.append(y_android[x_android.index(i)])
            else:
                android_data.append(0)
        return x, ios_data, android_data

    def ios_rate(self):
        data = self.GameRating.ios_rate()
        x_data = data.rdd.map(lambda x: str(int(x[1])) + '-' + str(int(x[1]) + 1)).collect()
        y_data = data.rdd.map(lambda x: int(x[0])).collect()
        return x_data, y_data

    def android_rate(self):
        data = self.GameRating.android_rate()
        x_data = data.rdd.map(lambda x: str(int(x[1])) + '-' + str(int(x[1]) + 1)).collect()
        y_data = data.rdd.map(lambda x: int(x[0])).collect()
        return x_data, y_data

