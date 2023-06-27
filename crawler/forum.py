# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-27 16:56
@Auth ： hyuRen
"""

import urllib.error
import urllib.request
import json
import csv
from json import JSONDecodeError

class Forum:
    def __init__(self):
        self.base_url = "https://www.taptap.cn/webapiv2/groups/game?X-UA=V%3D1%26PN%3DWebApp%26LANG%3Den-US%26VN_CODE" \
                        "%3D101%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dffa4c2c9-ce96-4b18-b2ef" \
                        "-86cdce779912%26VID%3D319851075%26DT%3DPC%26OS%3DWindows%26OSV%3D14.0.0"

        self.save_data = 'tap/forum.csv'

        self.head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/114.0.0.0 Safari/537.36"
        }

        self.uri = "https://www.taptap.cn"

    def get_data(self, base_url):
        data_list = []
        for i in range(5):
            try:
                url = self.base_url + f'&from={i*20}' + '&limit=20'
                response = self.ask_url(url)
                response = json.loads(response)
            except JSONDecodeError:
                return []
            data = response['data']['list']

            for item in data:
                dt = []
                try:
                    name = item['title']
                    dt.append(name)

                    website = item['web_url']
                    dt.append(self.uri + website)

                    favorite_count = item['stat']['favorite_count']
                    dt.append(favorite_count)

                    feed_count = item['stat']['feed_count']
                    dt.append(feed_count)

                    image_url = item['icon']['url']
                    dt.append(image_url)

                    data_list.append(dt)
                except KeyError:
                    pass

        return data_list


    def ask_url(self, url):
        request = urllib.request.Request(url=url, headers=self.head)
        html = ""
        try:
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf-8')
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
        return html


    def save_data(self, data_list, save_path):
        with open(save_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['forum_name', 'website', 'fans_count', 'feed_count', 'image_url'])
            for data in data_list:
                writer.writerow(data)