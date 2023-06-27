# -*- coding: utf-8 -*-
"""
@Time ： 2023-06-27 15:10
@Auth ： hyuRen
"""

import urllib.error
import urllib.request
import json
import csv
from json import JSONDecodeError

class Developer:
    def __init__(self):
        self.base_url = "https://www.taptap.cn/webapiv2/developer-top/v1/hits?X-UA=V%3D1%26PN%3DWebApp%26LANG%3Den-US" \
               "%26VN_CODE%3D101%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Dffa4c2c9-ce96-4b18-b2ef" \
               "-86cdce779912%26VID%3D319851075%26DT%3DPC%26OS%3DWindows%26OSV%3D14.0.0&from=0&limit=50"

        self.save_data = 'tap/developer.csv'

        self.head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/114.0.0.0 Safari/537.36"
        }

    def get_data(self, base_url):
        data_list = []
        try:
            response = self.ask_url(base_url)
            response = json.loads(response)
        except JSONDecodeError:
            return []

        data = response['data']['list']

        for item in data:
            dt = []
            try:
                name = item['name']
                dt.append(name)

                website = item['website']
                dt.append(website)

                app_count = item['stat']['app_count']
                dt.append(app_count)

                fans_count = item['stat']['fans_count']
                dt.append(fans_count)

                image_url = item['avatar']['url']
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
            writer.writerow(['company_name', 'website', 'app_count', 'fans_count', 'image_url'])
            for data in data_list:
                writer.writerow(data)