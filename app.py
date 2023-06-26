from flask import Flask, redirect, url_for

from my_flask.download_list import DownloadList
from my_flask.pop_list import PopList
from my_flask.game_type_num import GameTypeNum
from my_flask.get_rating import Rating

class App:
    def __init__(self):
        self.Pop = PopList()
        self.TypeNum = GameTypeNum()
        self.Rating = Rating()
        self.DownLoadList = DownloadList()
        self.app = Flask(__name__)
        self.app.add_url_rule('/pop/ios', view_func=self.Pop.ios_hot_list)
        self.app.add_url_rule('/pop/android', view_func=self.Pop.android_hot_list)
        self.app.add_url_rule('/type/num', view_func=self.TypeNum.get_type_num)
        self.app.add_url_rule('/game/rate', view_func=self.Rating.rating_top10)
        self.app.add_url_rule('/download/ios', view_func=self.DownLoadList.ios_download_num)
        self.app.add_url_rule('/download/android', view_func=self.DownLoadList.android_download_num)

        @self.app.route('/')
        def index():
            return redirect(url_for('ios_hot_list'))

    def run(self):
        self.app.run(host='192.168.10.100', port=5000, debug=True)


if __name__ == '__main__':
    app = App()
    app.run()
