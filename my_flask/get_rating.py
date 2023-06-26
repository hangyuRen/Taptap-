# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-24 16:28
@Auth ： hyuRen
"""
from flask import render_template

from my_flask.models import game_rating
class Rating:
    def __init__(self):
        self.GameRating = game_rating.GameRating()

    def rating_top10(self):
        x_ios, y_ios, x_android, y_android = self.GameRating.rating_top10()
        return render_template("line-gradient.html", x_ios=x_ios, y_ios=y_ios, x_android=x_android, y_android=y_android)