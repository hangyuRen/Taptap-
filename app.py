import re

import requests
from flask import Flask, redirect, render_template, request, make_response

from crawler.developer import Developer
from crawler.forum import Forum
from my_flask.download_list import DownloadList
from my_flask.fans_list import FansList
from my_flask.hot_list import PopList
from my_flask.models.hot_type import HotTypePercent
from my_flask.models.recommend import game_recommend
from my_flask.type_list import GameTypeNum
from my_flask.rating_list import Rating
from flask_cors import CORS

class App:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, supports_credentials=True)
        self.Pop = PopList()
        self.TypeNum = GameTypeNum()
        self.Rating = Rating()
        self.DownLoadList = DownloadList()
        self.FansList = FansList()
        self.HotTypePercent = HotTypePercent()

        @self.app.route('/')
        def redirect_to_initial():
            return redirect('/index')

        @self.app.route('/analytics')
        def page1():
            ios_game_fans, ios_fans, android_game_fans, android_fans = self.FansList.fans_list()
            ios_game_down, ios_down, android_game_down, android_down = self.DownLoadList.download_list()
            x_label, ios_rate, android_rate = self.Rating.rating()
            return render_template('analytics.html', ios_game_fans=ios_game_fans, ios_fans=ios_fans,
                                   android_game_fans=android_game_fans, android_fans=android_fans,
                                   ios_game_down=ios_game_down, ios_down=ios_down,
                                   android_game_down=android_game_down, android_down=android_down,
                                   x_label=x_label, ios_rate=ios_rate, android_rate=android_rate)

        @self.app.route('/index', methods=['GET', 'POST'])
        def home():
            ios_data_list = self.Pop.ios_hot_list()
            android_data_list = self.Pop.android_hot_list()

            type_list, num_list = self.TypeNum.get_type_num()

            developer = Developer()
            data_developer = developer.get_data(developer.base_url)
            forum = Forum()
            data_forum = forum.get_data(forum.base_url)
            hotest_type = self.HotTypePercent.get_hot_type_percent()

            return render_template('index.html', ios_data_list=ios_data_list, android_data_list=android_data_list,
                                   type_list=type_list, num_list=num_list, data_developer=data_developer,
                                   data_forum=data_forum,
                                   data_hottype=hotest_type)

        @self.app.route('/data-table')
        def page2():
            return render_template('recommend-list.html')

        # 基于获得的历史游戏信息，建立针对性的推荐列表
        @self.app.route('/get_recommend_list', methods=['GET', 'POST'])
        def update_table_data():
            # 获取用户输入的游戏名称
            game_like = request.form.get('game_like')

            # 将输入的游戏名称以逗号分隔，并转换为列表形式
            # 使用正则表达式分割游戏名称
            game_names = re.split(r',|，|\s|；|;|、', game_like)

            # print(game_names)
            # 根据推荐算法得到推荐的游戏数据，按推荐程度由高到低排序
            recommend_games = game_recommend(game_names)
            if recommend_games == -1:
                return render_template('recommend-list.html', error=recommend_games
                                       )
            # 使用collect()方法将Spark DataFrame中的数据收集到Python列表
            data_list = recommend_games.take(30)

            # 将收集到的数据列表转换为字典的列表形式
            table_data = [row.asDict() for row in data_list]

            return render_template('recommend-list.html', recommend_data=table_data)

        # 为解决显示图片的跨域问题，增加代理图片请求
        @self.app.route('/proxy_image', methods=['GET'])
        def proxy_image():
            image_url = request.args.get('url')  # 获取图片链接参数

            if image_url:
                # 发送HTTP GET请求获取图片数据
                response = requests.get(image_url)

                # 创建响应对象，设置响应头部信息
                proxy_response = make_response(response.content)
                proxy_response.headers.set('Content-Type', response.headers.get('Content-Type'))

                return proxy_response

            return 'Image URL not provided', 400  # 如果未提供图片链接参数，返回错误信息

    def run(self):
        self.app.run(host='192.168.10.100', port=5000, debug=True)

if __name__ == '__main__':
    app = App()
    app.run()
